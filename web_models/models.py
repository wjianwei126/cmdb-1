#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django.db import models
import datetime


class UserType(models.Model):
    caption = models.CharField(max_length=32)
    code = models.CharField(max_length=32)

    def __unicode__(self):
        return self.caption

class UserProfile(models.Model):

    user_type = models.ForeignKey('UserType')
    name = models.CharField(u'名字', max_length=32)
    email = models.EmailField(u'邮箱')
    phone = models.CharField(u'座机', max_length=50)
    mobile = models.CharField(u'手机', max_length=32)


    memo = models.TextField(u'备注', blank=True)
    create_at = models.DateTimeField(blank=True, auto_now_add=True)
    update_at = models.DateTimeField(blank=True, auto_now=True)

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = "用户信息"

    def __unicode__(self):
        return self.name


class AdminInfo(models.Model):
    user_info = models.OneToOneField(UserProfile)
    username = models.CharField(u'用户名', max_length=256)
    password = models.CharField(u'密码', max_length=256)


class Status(models.Model):
    name = models.CharField(max_length=64)
    code = models.CharField(max_length=64)
    memo = models.TextField(u'备注', null=True, blank=True)

    def __unicode__(self):
        return self.name


class DeviceType(models.Model):

    name = models.CharField(max_length=128)
    code = models.CharField(max_length=64)
    memo = models.CharField(max_length=256,null=True,blank=True)
    create_at = models.DateTimeField(blank=True, auto_now_add=True)
    update_at = models.DateTimeField(blank=True, auto_now=True)

    def __unicode__(self):
        return self.name


class Tag(models.Model):

    name = models.CharField('Tag name', max_length=32, unique=True)

    memo = models.TextField(u'备注', blank=True)
    create_at = models.DateTimeField(blank=True, auto_now_add=True)
    update_at = models.DateTimeField(blank=True, auto_now=True)

    def __unicode__(self):
        return self.name


class Asset(models.Model):
    device_type = models.ForeignKey('DeviceType')

    device_status = models.ForeignKey('Status')

    cabinet_num = models.CharField(u'机柜号', max_length=30, null=True, blank=True)
    cabinet_order = models.CharField(u'机柜中序号', max_length=30, null=True, blank=True)

    memo = models.TextField(u'备注', null=True, blank=True)
    create_at = models.DateTimeField(blank=True, auto_now_add=True)
    update_at = models.DateTimeField(blank=True, auto_now=True)

    idc = models.ForeignKey('IDC', verbose_name=u'IDC机房', null=True, blank=True)
    contract = models.ForeignKey('Contract', verbose_name=u'合同', null=True, blank=True)
    business_unit = models.ForeignKey('BusinessUnit', verbose_name=u'属于的业务线', null=True, blank=True)

    manage_user = models.ForeignKey('UserProfile', verbose_name=u'基础运维', related_name='+', null=True, blank=True)

    tag = models.ManyToManyField('Tag', null=True, blank=True)

    latest_date = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = '资产总表'
        verbose_name_plural = "资产总表"

    def __unicode__(self):
        try:
            manage_ip = self.server.manage_ip
        except: 
            manage_ip = '0.0.0.0'
        return manage_ip


class Server(models.Model):
    asset = models.OneToOneField('Asset')

    hostname = models.CharField(max_length=128, blank=True, null=True)
    service_sn = models.CharField(u'快速服务编码', max_length=128, blank=True,null=True)
    sn = models.CharField(u'SN号', max_length=64, blank=True, null=True)
    manufactory = models.CharField(verbose_name=u'制造商', max_length=128, null=True, blank=True)
    model = models.CharField(u'型号', max_length=128, null=True, blank=True)


    manage_ip = models.GenericIPAddressField(u'管理IP',null=True, blank=True)
    business_ip = models.GenericIPAddressField(u'业务IP',null=True, blank=True)

    os_platform = models.CharField(u'系统', max_length=64, null=True, blank=True)
    os_version = models.CharField(u'系统版本', max_length=64, null=True, blank=True)

    cpu_count = models.IntegerField(u'CPU核心数',null=True, blank=True)
    cpu_physical_count = models.IntegerField(u'物理CPU数',null=True, blank=True)
    cpu_model = models.CharField(max_length=128, null=True, blank=True)

    first_mac = models.CharField(u'MAC地址',max_length=128, null=True, blank=True)

    create_at = models.DateTimeField(blank=True, auto_now_add=True)
    update_at = models.DateTimeField(blank=True, auto_now=True)

    class Meta:
        verbose_name = '服务器'
        verbose_name_plural = "服务器"
        index_together = ["sn", "asset"]

    def __unicode__(self):
        return '%s,%s,%s,%s,%s,%s,%s' %(self.hostname,self.sn,self.manufactory,self.model,self.cpu_count,self.cpu_physical_count,self.cpu_model)


class OsInstall(models.Model):
    hostname = models.CharField(max_length=128)
    ip = models.GenericIPAddressField()
    server = models.ForeignKey('Server')
    creator = models.ForeignKey('UserProfile')
    create_at = models.DateTimeField(blank=True, auto_now_add=True)


class NetworkDevice(models.Model):
    asset = models.OneToOneField('Asset')
    sn = models.CharField(u'SN号',max_length=64,unique=True)

    asset = models.OneToOneField('Asset')
    management_ip = models.CharField(u'管理IP',max_length=64,blank=True,null=True)
    vlan_ip = models.CharField(u'VlanIP',max_length=64,blank=True,null=True)
    intranet_ip = models.CharField(u'内网IP',max_length=128,blank=True,null=True)
    sn = models.CharField(u'SN号',max_length=64,unique=True)
    manufactory = models.CharField(verbose_name=u'制造商',max_length=128,null=True, blank=True)
    model = models.CharField(u'型号',max_length=128,null=True, blank=True )
    port_num = models.SmallIntegerField(u'端口个数',null=True, blank=True )
    device_detail = models.TextField(u'设置详细配置',null=True, blank=True )
    class Meta:
        verbose_name_plural = "网络设备"
        verbose_name = '网络设备'


class Memory(models.Model):

    slot = models.CharField(u'插槽位',max_length=32,blank=True)
    manufactory = models.CharField(u'制造商', max_length=32,null=True,blank=True)
    model = models.CharField(u'型号', max_length=64,blank=True)
    capacity =  models.FloatField(u'容量',blank=True)
    sn = models.CharField(max_length=256,null=True,blank=True,default='')
    speed = models.CharField(max_length=64,null=True,blank=True,default='')
    memo = models.TextField(u'备注', blank=True)
    create_at = models.DateTimeField(blank=True, auto_now_add=True)
    update_at = models.DateTimeField(blank=True, auto_now=True)
    server_info = models.ForeignKey('server')

    class Meta:
        verbose_name = '内存部件'
        verbose_name_plural = "内存部件"

    def __unicode__(self):
        return '%s: %sGB '%( self.slot, self.capacity)


class NIC(models.Model):
    name = models.CharField(u'网卡名称',max_length=128,blank=True)
    hwaddr = models.CharField(u'网卡mac地址', max_length=64)
    up = models.BooleanField(default=False)
    netmask = models.CharField(max_length=64,blank=True)

    ipaddrs = models.CharField(u'ip地址',max_length=256,null=True)

    memo = models.TextField(u'备注', blank=True)
    create_at = models.DateTimeField(blank=True, auto_now_add=True)
    update_at = models.DateTimeField(blank=True, auto_now=True)

    server_info = models.ForeignKey('server')

    class Meta:
        verbose_name = '网卡部件'
        verbose_name_plural = "网卡部件"

    def __unicode__(self):
        return u'网卡%s --> MAC:%s;IP%s;up:%s;netmask:%s' %(self.name,self.hwaddr,self.ipaddrs,self.up,self.netmask)


class Disk(models.Model):

    slot = models.CharField(u'插槽位',max_length=32,blank=True)

    model = models.CharField(u'磁盘型号', max_length=128,blank=True)
    capacity = models.FloatField(u'磁盘容量GB',blank=True)
    pd_type = models.CharField(u'磁盘类型', max_length=64,blank=True)

    memo = models.TextField(u'备注', blank=True)
    create_at = models.DateTimeField(blank=True, auto_now_add=True)
    update_at = models.DateTimeField(blank=True, auto_now=True)

    server_info = models.ForeignKey('server')

    def __unicode__(self):
        return 'slot:%s size:%s' % (self.slot,self.capacity)


class IDC(models.Model):
    region = models.CharField(u'区域中文',max_length=64)
    name = models.CharField(u'中文显示名',max_length=32)
    floor = models.IntegerField(u'楼层',default=1)
    display = models.CharField(max_length=128)
    memo = models.CharField(u'备注',max_length=64)

    def __unicode__(self):
        return 'region:%s idc:%s floor:%s' %(self.region,
                                                    self.name,
                                                    self.floor)

    class Meta:
        verbose_name = '机房'
        verbose_name_plural = "机房"


class Contract(models.Model):
    sn = models.CharField(u'合同号', max_length=64,unique=True)
    name = models.CharField(u'合同名称', max_length=64 )
    cost = models.IntegerField(u'合同金额')
    start_date = models.DateTimeField(blank=True)
    end_date = models.DateTimeField(blank=True)
    license_num = models.IntegerField(u'license数量', blank=True)
    memo = models.TextField(u'备注', blank=True)
    create_at = models.DateTimeField(blank=True, auto_now_add=True)
    update_at = models.DateTimeField(blank=True, auto_now=True)

    class Meta:
        verbose_name = '合同'
        verbose_name_plural = "合同"

    def __unicode__(self):
        return self.name


class BusinessUnit(models.Model):
    name = models.CharField(u'业务线',max_length=64, unique=True)
    contact = models.ForeignKey('UserProfile',default=None)
    memo = models.CharField(u'备注',max_length=64, blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = '业务线'
        verbose_name_plural = "业务线"


class HandleLog(models.Model):
    asset_info = models.ForeignKey('Asset')
    content = models.TextField(null=True, blank=True)
    creator = models.ForeignKey('UserProfile')
    create_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.content


class ErrorLog(models.Model):
    name = models.CharField(max_length=256)


