from django.db.models import Sum,Q,Count
from api_data.models import TmpSite
from django.conf import settings
import datetime
__all__ = []





def dado_sla_total_devolvido(queryset,**kwargs):
        return queryset.annotate(entregue_prazo=Sum("qtde", filter=Q(tipo_baixa="ENTREGUE") and Q(sla="No prazo")),
                    entregue=Sum("qtde", filter=Q(tipo_baixa="ENTREGUE")), total=Sum("qtde"),
                    devolvido=Sum("qtde", filter=~Q(tipo_baixa="ENTREGUE")),
                    # entregue_d1 = Sum("qtde",filter=Q(entregas_d_mais="entregue_d1")),
                    # entregue_d2 = Sum("qtde",filter=Q(entregas_d_mais="entregue_d2")),
                    # entregue_d3 = Sum("qtde",filter=Q(entregas_d_mais="entregue_d3")),
                    # entregue_d4 = Sum("qtde",filter=Q(entregas_d_mais="entregue_d4")),
                    # entregue_d5 = Sum("qtde",filter=Q(entregas_d_mais="entregue_d5")),
                    # entregue_d6 = Sum("qtde",filter=Q(entregas_d_mais="entregue_d6")),
                    # entregue_d7 = Sum("qtde",filter=Q(entregas_d_mais="entregue_d7")),
                    # entregue_acima_d7 = Sum("qtde",filter=Q(entregas_d_mais="entregue_acima_d7")
                    #                                        ),
                                 **kwargs
                                 )
def adicionar_zero(item):
    item = str(item)
    if len(item) == 1:
        return "0%s"%(item)
    return item
def controle_data_mes(item):

    mes = item % 12
    if mes <= 0:
        return  12 - mes
    return mes

def controle_data_ano(item):

    if item <= 0:

        return -1

    return 0




class Sla_total_devolvido():
    def __init__(self,periodo,cliente):
        self.__periodo = periodo
        self.cliente = cliente
        self.definir_query()



    @property
    def periodo(self):
        if not isinstance(self.__periodo, datetime.datetime):
            raise ValueError("O formato nã é datatime.datatime")
        date_month_year = [self.__periodo.month, self.__periodo.year]
        periodo = []
        for item in range(0, 6):
            print(date_month_year[0],item)
            mes = date_month_year[0] - item
            print(mes)

            string_periodo = "%s/%s/%s" % ("01", adicionar_zero(controle_data_mes(mes)) , date_month_year[1] + controle_data_ano(mes))
            periodo.append(string_periodo)

        print(periodo)
        return periodo

    def definir_query(self):
        self.query_set = TmpSite.objects.using(settings.NAME_DB_FLASH).filter(data_post__in=self.periodo,cliente_id=self.cliente).values()

    def get_all_type_col(self,col,return_count=False):
        filter = {"%s__isnull"%col:False,}
        if return_count:
            return self.query_set.values(col,).filter(**filter).annotate(count=Count("cliente_id")).order_by('-count',)
        return self.query_set.values(col, ).filter(**filter).distinct()
    def get_count_col(self,col,col_in_name=True):
        filter_col = {}
        annotate_kwarg = {}
        for item in self.get_all_type_col(col):
            filter_col[col] = item[col]
            annotate_kwarg["%s%s"%(str(col).replace(" ","_") +"_" if col_in_name else "",str(item[col]).replace(" ",""))] = Sum("qtde",filter=Q(**filter_col))

        return annotate_kwarg



    def get_sla_total_devolvido(self,*args):
        if args:
            for item_agr in args:
                if not item_agr in ["uf","tipo_postagem","data_post"]:
                    raise ValueError("Argumento invalido")

        obj_dict = self.get_count_col("mot_devolucao")
        obj_dict1 = self.get_count_col("baixa_via_rt")
        obj_dict2 = self.get_count_col("alvo")
        obj_dict3 = self.get_count_col("entregas_d_mais",col_in_name=False)
        obj_dict4 = self.get_count_col("data_post", col_in_name=False)

        for item_data in self.periodo:

            if not item_data in obj_dict4:
                return [{"msg":"Não existe"},]







        return {"periodo":self.periodo,"dataFlash":dado_sla_total_devolvido(queryset=self.query_set.values("cliente_id",*args),**obj_dict3,**obj_dict,**obj_dict1,**obj_dict2)}


    def last_six_months(f):
        def wrapper(*args):
            periodo = args[0].periodo
            mes = {}
            for item_periodo in periodo:
                mes[item_periodo] = f(data_post=periodo[item_periodo])
        return wrapper
