from django.conf.urls import url
from django.urls import path
from mapmanagement import views

app_name = 'mapmanagement'

urlpatterns = [
    # ex: /mapmanagement/
    url(r'^$', views.MapManagementView.as_view(), name='index'),
    url(r'^proxy/(?P<url>.*)$', views.proxy, name='proxy'),
    url(r'^get_featureid_from_sectionid/<str:sectionID>$', views.get_featureid_from_sectionid, name='get_featureid_from_sectionid'),
    path('getRenderedMapManagementIndex', views.RenderedMapManagementIndexView.as_view(), name='get_rendered_index'),
    url(r'^getMemorialLayers/', views.MemorialView.as_view(), name='get_memorials'),
    url(r'^getAllFeatures/', views.AllFeaturesView.as_view(), name='get_all_memorials'),
    url(r'^getMemorials/', views.MemorialJsonView.as_view(), name='get_memorials'),
    url(r'^getGraveplots/', views.GraveplotView.as_view(), name='get_graveplots'),
    url(r'^getPersons/', views.PersonView.as_view(), name='get_persons'),
    url(r'^getPersonByMemorialID/', views.PersonByMemorialIDView.as_view(), name='get_person_by_memorial_id'),
    url(r'^findGraveplotByGraveNumber/', views.FindGraveplotByGraveNumberView.as_view(), name='get_person_by_graveplot_id'),
    url(r'^getPersonByID/', views.PersonsByIDsView.as_view(), name='get_person_by_id'),
    url(r'^getAllMemorialInscriptions/', views.AllMemorialInscriptionsView.as_view(), name='get_all_memorial_inscriptions'),
    #TODO: is .as_view the best way to do this? look it up. PlotNumberView
    path('mapSearch/', views.MapSearchView.as_view(), name="search_persons"),
    path('includeGravesInSearch/', views.IncludeGravesInSearchView.as_view()),
    path('burialNumber/', views.BurialNumberView.as_view()),
    url(r'^searchPublicPersonCompany/', views.PublicPersonCompanySearchView.as_view(), name="search_public_person_company"),
    url(r'^createNewBurial/', views.CreateNewBurialView.as_view(), name="create_new_burial"),
    url(r'^getBurialOfficials/', views.BurialOfficialsView.as_view(), name="burial_officials"),
    url(r'^addHeadstone/', views.AddHeadstoneView.as_view(), name="add_headstone"),
    url(r'^linkHeadstonePlot/', views.LinkHeadstonePlotView.as_view(), name="add_headstone"),
    url(r'^deleteHeadstone/', views.DeleteHeadstoneView.as_view(), name="delete_headstone"),
    url(r'^mapInitialisation/', views.MapInitialisationView.as_view(), name="map_initialisation"),
    url(r'^getReservedPersons/', views.ReservedPersonsView.as_view(), name="reserve_persons"),
    url(r'^getReservedGraveplots/', views.ReservedGraveplotsView.as_view(), name="reserved_graveplots_view"),
    url(r'^getLayerGroups/', views.LayerGroupsView.as_view(), name="layer_groups_view"),
    url(r'^siteFiles/', views.SiteFilesView.as_view(), name="site_files"),
    url(r'^takePhoto/', views.TakePhotoView.as_view(), name="take_photo"),
    url(r'^memorialInspection/', views.MemorialInspectionView.as_view(), name="memorial_inspection"),
    url(r'^getMemorialImages/', views.GetMemorialImages.as_view(), name="get_memorial_images"),
    url(r'^deleteMemorialImage/', views.DeleteMemorialImage.as_view(), name="delete_memorial_image"),
    url(r'^sendReport/', views.SendReport.as_view(), name="send_report"),
    url(r'^graveLinks/', views.GraveLinkView.as_view(), name="grave_link"),
    url(r'^modifyBurialsLinkedFeatures/', views.ModifyBurialsLinkedFeaturesView.as_view(), name="modify_burials_linked_features"),
    url(r'^getGraveNumbers/', views.GraveNumbersView.as_view(), name="gravenumbers"),
    url(r'^getSection/', views.SectionViewById.as_view(), name="section_by_sectionid"),
    url(r'^getSections/', views.SectionView.as_view(), name="section"),
    url(r'^getSubsections/', views.SubsectionView.as_view(), name="subsection"),
    url(r'^getFeatureIDs/', views.FeatureIDView.as_view(), name="featureid"),
    url(r'^graveDetails/', views.GraveDetailsView.as_view(), name="get_grave_details"),
    url(r'^graveDeedsList/', views.GraveDeedsListView.as_view(), name="get_grave_deeds_list"),
    url(r'^graveDeed/', views.GraveDeedView.as_view(), name="get_grave_deed"),
    url(r'^graveOwner/', views.GraveOwnerView.as_view(), name="get_grave_owner"),
    url(r'^createNewOwner/', views.CreateNewOwnerView.as_view(), name="create_new_owner"),
    url(r'^personroles/', views.PersonRolesView.as_view(), name="get_person_roles"),
    url(r'^companyroles/', views.CompanyRolesView.as_view(), name="get_company_roles"),
    url(r'^personownership/', views.PersonOwnershipView.as_view(), name="get_person_ownership"),
    url(r'^companyownership/', views.CompanyOwnershipView.as_view(), name="get_company_ownership"),
    url(r'^personNextOfKinTo/', views.PersonNextOfKinToView.as_view(), name="get_person_next_of_kin_to"),
    url(r'^relatedBurials/', views.RelatedBurialsView.as_view(), name="get_related_burials"),
    url(r'^relatedReservations/', views.RelatedReservationsView.as_view(), name="get_related_reservations"),
    url(r'^availablePlotGravePlot/', views.AvailablePlotGravePlotView.as_view(), name="available_plot_graveplot"),
    url(r'^getGraveplotLayer/', views.GetGraveplotLayerView.as_view(), name="get_graveplot_layer"),
    url(r'^relatedMemorials/', views.RelatedMemorialsView.as_view(), name="get_related_memorials"),
    url(r'^newGraveNumberCheck/', views.NewGraveNumberCheckView.as_view(), name="new_grave_number_check"),
    url(r'^allGravePlotOptions/', views.AllGravePlotOptionsView.as_view(), name="all_graveplot_options"),
    url(r'^allOwnershipOptions/', views.AllOwnershipOptionsView.as_view(), name="all_ownership_options"),
    #url(r'^allPersonOptions/', views.AllPersonOptionsView.as_view(), name="all_person_options"),
    url(r'^allBurialOptions/', views.AllBurialOptionsView.as_view(), name="all_burial_options"),
    url(r'^memorialDetails/', views.MemorialDetailsView.as_view(), name="get_memorial_details"),
    url(r'^relatedPersons/', views.RelatedPersonsView.as_view(), name="get_related_persons"),
    url(r'^basicPerson/', views.BasicPersonView.as_view(), name="get_basic_person"),
    url(r'^personDetail/', views.DeathPersonDetailView.as_view(), name="get_person_details"),
    url(r'^convertReservation/', views.ConvertReservationToBurialView.as_view(), name="convert_reservation"),
    url(r'^burialInformation/', views.BurialInformationView.as_view(), name="get_burial_information"),
    url(r'^burialDetails/', views.BurialDetailsView.as_view(), name="get_burial_details"),
    url(r'^moveBurialPersonRecords/', views.MoveBurialPersonRecordsView.as_view(), name="move_burial_person_records"),
    url(r'^removeBurialPersonRecords/', views.RemoveBurialPersonRecordsView.as_view(), name="remove_burial_person_records"),
    url(r'^deleteBurialPersonRecords/', views.DeleteBurialPersonRecordsView.as_view(), name="delete_burial_person_records"),
    url(r'^featureAttributes/', views.FeatureAttributesView.as_view()),
    url(r'^featureAttributesExist/', views.FeatureAttributesExistView.as_view()),
    url(r'^addAvailablePlot/', views.AddAvailablePlot.as_view()),
    url(r'^updatePlot/', views.UpdatePlot.as_view()),
    url(r'^updateMemorial/', views.UpdateMemorial.as_view()),
    url(r'^deletePlot/', views.DeletePlot.as_view()),
    path('unlinkedBurialsWithTranscribedGraveNumber/<str:grave_number>/', views.UnlinkedBurialsWithTranscribedGraveNumberView.as_view()),
]