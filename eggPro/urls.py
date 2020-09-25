"""eggPro URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
import egg.views as egg
import vitamin.views as vitamin
import doupo.views as doupo
import futures.views as futures
import yumi.views as yumi

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',egg.index,name='index'),
    path('login/',egg.acc_login,name='login'),
    path('welcome/',egg.welcome,name='welcome'),
    path('dailyPrice/',egg.daily_egg_price,name='dailyPrice'),
    path('ajaxSelectTypeDailyPrice/',egg.ajax_select_daily_price,name='ajaxSelectTypeDailyPrice'),
    path('ajaxDailyPrice/',egg.ajax_egg_daily_price,name='ajaxDailyPrice'),
    path('weeklyPrice/',egg.weekly_egg_price,name='weeklyPrice'),
    path('monthlyPrice/',egg.monthly_egg_price,name='monthlyPrice'),
    path('weeklyOutput/',egg.weekly_egg_output,name='weeklyOutput'),
    path('ajaxWeeklyOutput/',egg.ajax_weekly_egg_output,name='ajaxWeeklyOutput'),
    path('monthlyOutput/',egg.monthly_egg_output,name='monthlyOutput'),
    path('yearlyOutput/',egg.yearly_egg_output,name='yearlyOutput'),
    path('weeklyCost/',egg.weekly_egg_cost,name='weeklyCost'),
    path('monthlyCost/',egg.monthly_egg_cost,name='monthlyCost'),
    path('weeklyProfit/',egg.weekly_egg_profit,name='weeklyProfit'),
    path('monthlyProfit/',egg.monthly_egg_profit,name='monthlyProfit'),
    path('qihuo/',egg.qihuo_zhuli,name='qihuo'),
    path('qihuoZijin/',egg.qihuo_zijin_info,name='qihuoZijin'),
    path('ajaxWkVitaminPrice/',vitamin.ajax_get_vitamin_weekly_price,name='ajaxWkVitaminPrice'),
    path('ajaxDailyPriceDoupo/',doupo.ajax_daily_doupo_price,name='ajaxDailyPriceDoupo'),
    path('ajaxFuturesPrice/',futures.ajax_get_futures_info,name='ajaxFuturesPrice'),
    path('ajaxDailyPriceYumi/',yumi.ajax_daily_yumi_price,name='ajaxDailyPriceYumi'),
    path('yuceEggChanliang/',egg.yuce_egg_chanliang,name='yuceEggChanliang'),
    path('yuceEggPrice/',egg.yuce_egg_price,name='yuceEggPrice'),
    path('yuceSpdChujiCL/',egg.yuce_shangpindai_chuji_chanliang,name='yuceSpdChujiCL'),
    path('yuceTaojiShuliang/',egg.yuce_taoji_shuliang,name='yuceTaojiShuliang'),
    path('yuceFmdYCcunlan/',egg.yuce_fmd_yucheng_cunlan,name='yuceFmdYCcunlan'),
    path('yuceFmdCDcunlan/',egg.yuce_fmd_chandan_cunlan,name='yuceFmdCDcunlan'),
    path('yuceSpdYCcunlan/',egg.yuce_spd_yucheng_cunlan,name='yuceSpdYCcunlan'),
    path('yuceSpdCDcunlan/',egg.yuce_spd_chandan_cunlan,name='yuceSpdCDcunlan'),
    path('weeklySiliaoUsage/',egg.weekly_siliao_usage,name='weeklySiliaoUsage'),
    path('monthlySiliaoUsage/',egg.monthly_siliao_usage,name='monthlySiliaoUsage'),
    path('yearlySiliaoUsage/',egg.yearly_siliao_usage,name='yearlySiliaoUsage'),
    path('weeklyCostCalc/',egg.weekly_cost_calc,name='weeklyCostCalc')
]
