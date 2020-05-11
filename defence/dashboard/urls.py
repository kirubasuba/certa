from django.contrib import admin
from django.urls import path, include, re_path

from . import views
from . import do_views
from . import TAC_views,RD_views,CE_view
urlpatterns = [
    path('',views.dashboard, name="home"),
    re_path(r'^new_user/$', views.new_user, name="new_user"),
    re_path(r'^new_cemilac_user/$', views.new_cemilac_user, name="new_cemilac_user"),
    re_path(r'^viewunregistration/$', views.viewunregistration, name="viewunregistration"),
    re_path(r'^viewregistration/$', views.viewregistration, name="viewregistration"),
    re_path(r'^hold/$', views.hold, name="hold"),
    re_path(r'^newtypeapproval/$', views.newtypeapproval, name="newtypeapproval"),
    re_path(r'^id_gen/$', views.id_gen, name="id_gen"),
    re_path(r'^new_id_generate/$', views.new_id_generate, name="new_id_generate"),
    re_path(r'^upload_refdoc/$', views.upload_refdoc, name="upload_refdoc"),
    re_path(r'^doc_upload_views/$', views.doc_upload_views, name="doc_upload_views"),
    re_path(r'^upload_taapplication/$', views.upload_taapplication, name="upload_taapplication"),
    re_path(r'^fileview/$', views.fileView, name='fileview'),
    re_path(r'^pdf/$', views.generatepdf, name='pdf'),
    re_path(r'^proformapdf/$', do_views.generateproformapdf, name='proformapdf'),
    re_path(r'^process_proforma/$', do_views.process_proforma, name='process_proforma'),
    re_path(r'^RD_received/$', RD_views.RD_received, name='RD_received'),
    re_path(r'^TAC_received/$', TAC_views.TAC_received, name='TAC_received'),
    re_path(r'^TAC_forward_do/$', TAC_views.TAC_forward_do, name='TAC_forward_do'),
    re_path(r'^checklist/$', TAC_views.checklist, name='checklist'),
    re_path(r'^addchecklist/$', TAC_views.addchecklist, name='addchecklist'),
    re_path(r'^recommends_ta/$', RD_views.recommends_ta, name='recommends_ta'),
    # re_path(r'^approved/$', popview.approved.as_view(), name='approved'),
    re_path(r'^sign_pass/$', RD_views.sign_pass, name='sign_pass'),
    re_path(r'^sign_pass_TCSGD/$', RD_views.sign_pass_TCSGD, name='sign_pass_TCSGD'),
    re_path(r'^hold_remarks/$', views.hold_remarks, name='hold_remarks'),
    re_path(r'^comments/$', RD_views.comments, name='comments'),
    re_path(r'^allcomments/$', RD_views.allcomments, name='allcomments'),
    re_path(r'^doc_add/$',views.doc_add, name='doc_add'),
    re_path(r'^addanotherdoc/$',views.addanotherdoc, name='addanotherdoc'),
    re_path(r'^doc_change/$',views.doc_change, name='doc_change'),
    re_path(r'^ce_received/$',CE_view.ce_received, name='ce_received'),
    re_path(r'^gd_received/$',CE_view.gd_received, name='gd_received'),
    re_path(r'^tac_received/$',CE_view.tac_received, name='tac_received'),
    re_path(r'^do_received/$',CE_view.do_received, name='do_received'),
    re_path(r'^TAC_received_verified/$',CE_view.TAC_received_verified, name='TAC_received_verified'),
    re_path(r'^gd_received_verified/$',CE_view.gd_received_verified, name='gd_received_verified'),
    re_path(r'^ce_received_verified/$',CE_view.ce_received_verified, name='ce_received_verified'),
    re_path(r'^re_assign_to/$',TAC_views.re_assign_to, name='re_assign_to'),
    re_path(r'^send_otp/$',RD_views.send_otp, name='send_otp'),
    path('useredit/<int:id>/', views.user_edit, name='edit'),
    path('viewtyperecord/<int:id>/', do_views.viewtyperecord, name='viewtyperecord'),
    path('viewtyperecordbytac/<int:id>/', TAC_views.viewtyperecordbytac, name='viewtyperecordbytac'),
    path('viewtyperecordbyrd/<int:id>/', RD_views.viewtyperecordbyrd, name='viewtyperecordbyrd'),
    path('RD_forward_tac/<int:id>/', RD_views.RD_forward_tac, name='RD_forward_tac'),
    path('CE_forward_GD/<int:id>/', CE_view.CE_forward_GD, name='CE_forward_GD'),
    path('gd_forward_tac/<int:id>/', CE_view.gd_forward_tac, name='gd_forward_tac'),
    path('tac_forward_do/<int:id>/', CE_view.tac_forward_do, name='tac_forward_do'),
    path('DO_verified/<int:id>/', CE_view.DO_verified, name='DO_verified'),
    path('TAC_verified/<int:id>/', CE_view.TAC_verified, name='TAC_verified'),
    path('gd_verified/<int:id>/', CE_view.gd_verified, name='gd_verified'),
    path('addproforma/<int:id>/', do_views.addproforma, name='addproforma'),
    path('proformaviewbytac/<int:id>/', TAC_views.proformaviewbytac, name='proformaviewbytac'),
    path('proformaviewbyrd/<int:id>/', RD_views.proformaviewbyrd, name='proformaviewbyrd'),
    path('draft_ta/<int:id>/', do_views.draft_ta, name='draft_ta'),
    path('data_sheet/<int:id>/', do_views.data_sheet, name='data_sheet'),
    path('newchecklist/<int:id>/', TAC_views.newchecklist, name='newchecklist'),
    # path('approved/', RD_views.approved, name='approved'),
    path('rejected/<int:id>/', RD_views.rejected, name='rejected'),
    path('rowselect/<int:id>/', do_views.rowselect, name='rowselect'),
    path('pdfviewercopy/<int:id>/', do_views.pdfviewercopy, name='pdfviewercopy'),
    re_path(r'^dashboard_status/$', views.dashboard_status, name="dashboard_status"),
    re_path(r'^addcomment/$', do_views.addcomment, name="addcomment"),
    re_path(r'^reg_dashboard_status/$', views.reg_dashboard_status, name="reg_dashboard_status"),
    re_path(r'^password_reset/$',views.password_reset, name='password_reset'),
    re_path(r'^addcomment/$', do_views.addcomment, name="addcomment"),
    re_path(r'^actiontaken/$', do_views.actiontaken, name="actiontaken"),
    re_path(r'^viewcomment/$', do_views.viewcomment, name="viewcomment"),
    path('notification/', views.notification, name='notification'),
    path('closecomment/<int:id>/', do_views.closecomment, name='closecomment'),
    path('viewfile/<int:id>/', do_views.viewfile, name='viewfile'),



    
]

