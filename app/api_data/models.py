# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class TmpSite(models.Model):
    data_post = models.CharField(max_length=12, null=True)
    tipo_postagem = models.CharField(max_length=100, null=True)
    tipo_envio = models.CharField(max_length=100, null=True)
    cliente_id = models.IntegerField(primary_key=True)
    cliente = models.CharField(max_length=30, blank=True, null=True)
    ctt_id = models.IntegerField(blank=True, null=True)
    contrato = models.CharField(max_length=10, blank=True, null=True)
    entregas_d_mais = models.CharField(max_length=20, blank=True, null=True)
    uf = models.CharField(max_length=2, blank=True, null=True)
    tipo_baixa = models.CharField(max_length=20, null=True)
    sla = models.CharField(max_length=20, null=True)
    mot_devolucao_id = models.IntegerField(blank=True, null=True)
    mot_devolucao = models.CharField(max_length=20, blank=True, null=True)
    baixa_via_rt = models.CharField(max_length=20, null=True)
    alvo = models.CharField(max_length=20, null=True)
    tentativas = models.SmallIntegerField(blank=True, null=True)
    qtde = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tmp_site'
