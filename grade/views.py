import json

from django.shortcuts import render

# Create your views here.
from django.core.cache import cache
from django.views import View
from django import http


class GetGradeView(View):
    def get(self, request):
        # 参数获取
        port = request.GET.get('port')
        start = request.GET.get('start')
        end = request.GET.get('end')

        # 参数验证
        if not all([port, start, end]):
            return http.HttpResponseForbidden('参数缺失')

        # 数据库加载用户信息排序展示
        # users_list = 用户模型.objects.order_by('grade').all()[start:end+1]

        user_list = []
        # 遍历用户信息，数据构造
        # for user in users_list:
        #     user_list.append({
        #         'rank': user.rank,
        #         'port': user.port,
        #         'grade': user.grade
        #     })

        # 获取个人缓存数据
        mysort = cache.get(port)
        # 根据用户信息获取数据库内容
        # my = 用户模型.objects.filter(port=port).get()

        my_dict = {
            # 'rank': my.rank if my else '个人数据为空',
            'port': mysort.get('port') if mysort else '个人数据为空',
            'grade': mysort.get('grade') if mysort else '个人数据为空'
        }

        user_list.append(my_dict)

        data = {'data': user_list}
        return http.JsonResponse(data)

    def post(self, request):
        # 参数获取
        port = request.POST.get('port')
        grade = request.POST.get('grade')

        # 参数验证
        if not all([port, grade]):
            return http.HttpResponseForbidden('数据填写不完整')
        # 数据构造
        data = {
            'port': port,
            'grade': grade,
        }
        # 验证缓存中是否存在该数据
        port_cache = cache.get(port)
        if not port_cache:
            # 不存在，添加
            cache.set(port, data)

            # 数据库新增该角色信息
            # user = 用户模型(
            #   port = port
            #   grade = int(grade)
            # )
            # user.save()
        else:
            # 存在删除后添加新数据
            cache.delete(port)
            cache.set(port, data)

            # 更新数据库信息
            # 用户模型.objects.filter(port=port).update(grade=grade)

        return http.JsonResponse({'code': 200, 'errmsg': "OK"})
