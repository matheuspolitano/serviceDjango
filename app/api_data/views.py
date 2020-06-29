from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import TmpSite
from own_modules.data import Sla_total_devolvido
import datetime
from django.db.models import Q,F,Count,When,Case,Sum


class DataAPI(APIView):
    cliente = 4411
    db = "flash_db"
    def dado(self,func):
        return func.aggregate(entregue_prazo=Sum("qtde", filter=Q(tipo_baixa="ENTREGUE") and Q(sla="No prazo")),
                  entregue=Sum("qtde", filter=Q(tipo_baixa="ENTREGUE")), total=Sum("qtde"),
                  devolvido=Sum("qtde", filter=~Q(tipo_baixa="ENTREGUE")))

    def get(self,request):
        uf = []
        sla = Sla_total_devolvido(datetime.datetime.now(),cliente=4411)

        #sla.get_count_col("mot_devolucao")
        return Response(sla.get_sla_total_devolvido("uf","data_post","tipo_postagem"),status.HTTP_200_OK)

# Create your views here.
