from datetime import datetime

from django.conf import settings
from django.db import connection

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from geonode.data_upload.models import ScadaStatus
from geonode import settings as geonode_settings


# class ScadaApiView(APIView):
#
#     def post(self, request):
#         message = "Saved data successfully"
#         error = False
#
#         api_key = request.query_params.get('key')
#         if api_key != settings.SCADA_API_KEY:
#             return Response(data={'message': 'Api key does not match.', 'error': True}, status=status.HTTP_200_OK)
#
#         dtw_id = request.query_params.get('dtw_id')
#         with connection.cursor() as cur:
#             dtw_table = geonode_settings.layers_with_external_properties_settings['DTW']['name'].split(':')[1]
#             cur.execute("select dtw_id, dma_id, zone_id from datastore.{1} where dtw_id='{0}'".format(dtw_id, dtw_table))
#             row = cur.fetchone()
#
#         if not row:
#             return Response(data={'message': 'DTW id does not dmatches', 'error': True}, status=status.HTTP_200_OK)
#
#         reading = float(request.query_params.get('reading'))
#         timestamp = int(request.query_params.get('timestamp'))
#         scada_timestamp = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
#         zone_id = _value_formatter(int(row[2]), 2)
#         dma_id = _value_formatter(int(row[1]), 4)
#         scada_reading = ScadaReading(dtw_id=dtw_id, zone_id=zone_id, time_stamp=scada_timestamp, dma_id=dma_id, reading=reading)
#         scada_reading.save()
#
#         return Response(data={'message': message, 'error': error}, status=status.HTTP_200_OK)
# http://dwasa.streamstech.com/api/wasa/scada-reading?key=T8LbnjvZLzy2&dtw_id=1006014&reading=123&timestamp=1618829143


class ScadaStatusAPIView(APIView):
    # def post(self, request):
    #     message = "Saved data successfully"
    #     error = False
    #     api_key = request.query_params.get('key')
    #     global_status = globals()['status']
    #     if api_key != settings.SCADA_API_KEY:
    #         return Response(data={'message': 'Api key does not match.', 'error': True}, status=global_status.HTTP_200_OK)
    #     dtw_id = request.query_params.get('dtw_id')
    #     with connection.cursor() as cur:
    #         dtw_table = geonode_settings.layers_with_external_properties_settings['DTW']['name'].split(':')[1]
    #         cur.execute("select dtw_id, dma_id, zone_id from datastore.{1} where dtw_id='{0}'".format(dtw_id, dtw_table))
    #         row = cur.fetchone()
    #     area_name = request.query_params.get('area_name')
    #     status = request.query_params.get('status')
    #     frequency = float(request.query_params.get('frequency'))
    #     flow_rate = float(request.query_params.get('flow_rate'))
    #     water_level = float(request.query_params.get('water_level'))
    #     scada_timestamp = int(request.query_params.get('scada_timestamp'))
    #     scada_time = datetime.utcfromtimestamp(scada_timestamp).strftime('%Y-%m-%d %H:%M:%S')
    #     if not row:
    #         zone_id = _value_formatter(0, 2)
    #         dma_id  = _value_formatter(0, 2)
    #     else:
    #         zone_id = _value_formatter(int(row[2]), 2)
    #         dma_id = _value_formatter(int(row[1]), 4)
    #     scada_status = ScadaStatus(dtw_id=dtw_id, area_name=area_name, status=status, frequency=frequency, flow_rate=flow_rate, water_level=water_level, scada_time=scada_time, dma_id=dma_id, zone_id=zone_id)
    #     scada_status.save()
    #     return Response(data={'message': message, 'error': error}, status=global_status.HTTP_200_OK)

    def get(self, request):
        message = "Saved data successfully"
        error = False
        api_key = request.query_params.get('key')
        global_status = globals()['status']
        if api_key != settings.SCADA_API_KEY:
            return Response(data={'message': 'Api key does not match.', 'error': True}, status=global_status.HTTP_200_OK)
        dtw_id = request.query_params.get('dtw_id')
        with connection.cursor() as cur:
            dtw_table = geonode_settings.layers_with_external_properties_settings['DTW']['name'].split(':')[1]
            cur.execute("select dtw_id, dma_id, zone_id from datastore.{1} where dtw_id='{0}'".format(dtw_id, dtw_table))
            row = cur.fetchone()
        area_name = request.query_params.get('area_name')
        status = request.query_params.get('status')
        frequency = float(request.query_params.get('frequency'))
        flow_rate = float(request.query_params.get('flow_rate'))
        water_level = float(request.query_params.get('water_level'))
        scada_timestamp = int(request.query_params.get('scada_timestamp'))
        scada_time = datetime.utcfromtimestamp(scada_timestamp).strftime('%Y-%m-%d %H:%M:%S')
        if not row:
            zone_id ="not found"
            dma_id  ="not found"
        else:
            zone_id = _value_formatter(int(row[2]), 2)
            dma_id = _value_formatter(int(row[1]), 4)
        scada_status = ScadaStatus(dtw_id=dtw_id, area_name=area_name, status=status, frequency=frequency, flow_rate=flow_rate, water_level=water_level, scada_time=scada_time, dma_id=dma_id, zone_id=zone_id)
        scada_status.save()
        return Response(data={'message': message, 'error': error}, status=global_status.HTTP_200_OK)
# http://dwasa.streamstech.com/api/wasa/scada-status?key=T8LbnjvZLzy2&dtw_id=1005002&area_name=Uttora&status=RUNNING&frequency=3.4&flow_rate=5.4&water_level=2.4&scada_timestamp=1518829143



def _value_formatter(value, min_digit):
    formatted_value = str(value).zfill(min_digit)
    return formatted_value;