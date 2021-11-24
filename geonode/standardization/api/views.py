import logging

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from geonode.data_upload.api.services import get_data_upload_service
from geonode.data_upload.enums import MonthEnum, YEARS, ZoneEnum, DataTypeEnum
from geonode.data_upload.models import StatusUpdateModel, DmaZone, BulkMeterReading, UnbilledAuthorizedConsumption
from geonode.data_upload.models import CommercialLoss
from geonode.data_upload.tasks import save_file_data
from geonode.data_upload.store_procedure import *

logger = logging.getLogger(__name__)

data_upload_form_options = {
    "years": [],
    "months": [],
    "zones": [],
    "all_dma": [],
    "data_types": []
}


class ModelDataUploadFormOptionsAPIView(APIView):
    def get(self, request):
        return Response(data=data_upload_form_options, status=status.HTTP_200_OK)


class DataUploadFromFileAPIView(APIView):
    corrupted_file_message = "The file you are trying to upload might be corrupted"
    success_message = "Data uploading has been started.Please have a look at status update tab to see upload status"
    not_permitted_msg = 'You are not allowed to perform this operation'

    def post(self, request):

        user = request.user
        if not request.user.is_authenticated():
            return Response(data=self.not_permitted_msg, status=status.HTTP_403_FORBIDDEN)
        zone = request.data.get('zone', None)
        dma = request.data.get('dma', None)

        data_type = request.data.get('data_type', None)

        data_upload_service_class = get_data_upload_service(data_type)

        file_path, err = data_upload_service_class.get_file_path(request)
        if err:
            logger.error(err)
            return Response(data=err, status=status.HTTP_403_FORBIDDEN)
        try:
            data_upload_service = data_upload_service_class(user, zone, dma, file_path)
        except Exception as e:
            logger.error(str(e))
            return Response(data=self.corrupted_file_message, status=status.HTTP_403_FORBIDDEN)

        valid_data, msg = data_upload_service.is_valid()
        if not valid_data:
            logger.error(msg)
            return Response(data=msg, status=status.HTTP_403_FORBIDDEN)

        save_file_data(user.id, zone, dma, data_type, file_path)
        return Response(data=self.success_message, status=status.HTTP_200_OK)


class ModelDataUploadStatusAPIView(APIView):
    def get(self, request):
        status_updates = StatusUpdateModel.objects.all().order_by(
            '-date_created').values('id', 'file_name', 'uploader__username', 'date_updated', 'upload_status',
                                    'has_errors', 'file_type')
        return Response(data=status_updates, status=status.HTTP_200_OK)


class UploadErrorDetailsAPIView(APIView):
    def get(self, request, pk):
        status_update = StatusUpdateModel.objects.get(pk=pk)
        data = eval(status_update.errors)[:200]
        return Response(data=data, status=status.HTTP_200_OK)


class DmaZoneAPIView(APIView):
    def get(self, request):
        zone_dma_dict_list = []
        dma_zones = DmaZone.objects.all().order_by('zone_name')
        for dma_zone in dma_zones:
            existing_zone = None
            for index, item in enumerate(zone_dma_dict_list):
                if item['zone_id'] == dma_zone.zone_id:
                    existing_zone = item
                    break
            if existing_zone:
                zone_dma_dict_list[index]['dma_list'].append({
                    "dma_id": dma_zone.dma_id,
                    "dma_name": dma_zone.dma_name,
                })
            else:
                zone = {
                    "zone_id": dma_zone.zone_id,
                    "zone_name": dma_zone.zone_name,
                    "dma_list": [
                        {
                            "dma_id": dma_zone.dma_id,
                            "dma_name": dma_zone.dma_name,
                        }
                    ]
                }
                zone_dma_dict_list.append(zone)
        from operator import itemgetter
        for index, zone in enumerate(zone_dma_dict_list):
            sorted_list = sorted(zone["dma_list"], key=itemgetter('dma_name'))
            zone["dma_list"] = sorted_list
            zone_dma_dict_list[index] = zone
        return Response(data={"zones": zone_dma_dict_list}, status=status.HTTP_200_OK)


class BulkDmaUploadAPIView(APIView):
    def post(self, request):
        meter_id = request.data.get('meter_id')
        zone_id = request.data.get('zone_id')
        dma_id = request.data.get('dma_id')
        year_month = request.data.get('year_month')
        previous_reading = request.data.get('previous_reading')
        current_reading = request.data.get('current_reading')
        meter_adderss = request.data.get('meter_adderss')
        inflow = request.data.get('inflow')

        meter_reading_obj, created = BulkMeterReading.objects.get_or_create(meter_id=meter_id)
        meter_reading_obj.zone_id = zone_id
        meter_reading_obj.dma_id = dma_id
        meter_reading_obj.year_month = year_month
        meter_reading_obj.previous_reading = previous_reading
        meter_reading_obj.current_reading = current_reading
        meter_reading_obj.meter_address = meter_adderss
        meter_reading_obj.inflow = inflow

        meter_reading_obj.user_id = request.user.id
        meter_reading_obj.save()
        calculate_water_history_bulk_meter(dma_id, str(meter_reading_obj.year_month))
        return Response(data='saved data successfully', status=status.HTTP_200_OK)



class UacUploadAPIView(APIView):
    def post(self, request):
        obj = UnbilledAuthorizedConsumption(**request.data)
        obj.user_id = request.user.id
        obj.save()
        calculate_water_history_uac(str(obj.year_month))
        return Response(data='saved data successfully', status=status.HTTP_200_OK)


class CommercialLossUploadAPIView(APIView):
    def post(self, request):
        obj = CommercialLoss(**request.data)
        obj.user_id = request.user.id
        obj.save()
        calculate_water_history_commercial_loss(str(obj.year_month))
        return Response(data='saved data successfully', status=status.HTTP_200_OK)


class DmaBulkMeterDeleteAPIView(APIView):
    def post(self, request):
        message = "Deleted data successfully"
        error = False
        try:
            id = request.data.get('id')
            bulkMeterReading = BulkMeterReading.objects.get(id=id)
            dma_id = bulkMeterReading.dma_id
            year_month = bulkMeterReading.year_month
            bulkMeterReading.delete()
            calculate_water_history_bulk_meter(dma_id, year_month)
            return Response(data={'message': message, 'error': error}, status=status.HTTP_200_OK)

        except Exception as e:
            message = e.message
            error = True
            return Response(data={'message': message, 'error': error}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)