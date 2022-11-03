import Vue from 'vue'
import featureSidebarStore from '@/mapmanagement/store/modules/ManagementTool';
import store from '@/mapmanagement/store/index';
import VueRouter from 'vue-router';
import constants from '@/global-static/constants.ts';
import mapManagementConstants from '@/mapmanagement/static/constants.ts';

const ContentContainer = () => import('@/mapmanagement/components/ManagementTool/FormHelperComponents/ContentContainer.vue')
const BurialPersonManagement = () => import('@/mapmanagement/components/ManagementTool/Tools/BurialPersonManagement.vue')

const MemorialManagement = () => import('@/mapmanagement/components/ManagementTool/Tools/MemorialManagement.vue')
const PersonBurialDetails = () => import('@/mapmanagement/components/ManagementTool/Components/PersonBurialDetails');
const AddBurial = () => import('@/mapmanagement/components/ManagementTool/Components/AddBurial');
const MemorialDetails = () => import('@/mapmanagement/components/ManagementTool/Components/MemorialDetails');
const GraveLinkComponent = () => import('@/mapmanagement/components/MapTools/GraveLinkComponent');
const Photos = () => import('@/mapmanagement/components/MapTools/MemorialCaptureSidebar/Photos');

const GraveManagement = () => import('@/mapmanagement/components/ManagementTool/Tools/GraveManagement.vue')
const GraveDetails = () => import('@/mapmanagement/components/ManagementTool/Components/GraveDetails');
// const FeatureGeometry = () => import('@/mapmanagement/components/ManagementTool/Components/FeatureGeometry');
const LinkedMemorials = () => import('@/mapmanagement/components/ManagementTool/Components/LinkedMemorials.vue');
const GraveOwnership = () => import('@/mapmanagement/components/ManagementTool/Components/GraveOwnership');
const GraveOwner = () => import('@/mapmanagement/components/ManagementTool/Components/GraveOwner.vue');
const AddOwner = () => import('@/mapmanagement/components/ManagementTool/Components/AddOwner.vue');
const ConvertReservation = () => import('@/mapmanagement/components/ManagementTool/Components/ConvertReservation.vue');
const DeleteReservation = () => import('@/mapmanagement/components/ManagementTool/Components/DeleteReservation.vue');

const PersonManagement = () => import('@/mapmanagement/components/ManagementTool/Tools/PersonManagement.vue')
const PersonDetails = () => import('@/mapmanagement/components/ManagementTool/Components/PersonDetails.vue')
const Address = () => import('@/mapmanagement/components/ManagementTool/Components/Address.vue')
const PersonCompanyOwnership = () => import('@/mapmanagement/components/ManagementTool/Components/PersonCompanyOwnership.vue')
const PersonNextOfKinTo = () => import('@/mapmanagement/components/ManagementTool/Components/PersonNextOfKinTo.vue')

const CompanyManagement = () => import('@/mapmanagement/components/ManagementTool/Tools/CompanyManagement.vue')
const CompanyDetails = () => import('@/mapmanagement/components/ManagementTool/Components/CompanyDetails.vue')
const DeathPersonDetails = () => import('@/mapmanagement/components/ManagementTool/Components/DeathPersonDetails');

const FeatureManagement = () => import('@/mapmanagement/components/ManagementTool/Tools/FeatureManagement.vue');
const FeatureAttributes = () => import('@/mapmanagement/components/ManagementTool/Components/FeatureAttributes');
const FeatureSurveys = () => import('@/mapmanagement/components/ManagementTool/Components/Survey');

Vue.use(VueRouter);

const router = new VueRouter({
  routes: [
    {
      path: '/' + constants.GRAVE_MANAGEMENT_PATH + '/:id/:layer/:availablePlotID?',
      name: constants.GRAVE_MANAGEMENT_PATH,
      component: GraveManagement,
      children: [
        {
          path: 'o',
          name: 'graveManagementContainer',
          component: ContentContainer,
          children: [
            { 
              path: constants.GRAVE_MANAGEMENT_CHILD_ROUTES.burials + '/:burial_id/:person_id',
              name: constants.GRAVE_MANAGEMENT_CHILD_ROUTES.burials,
              component: PersonBurialDetails,
              props: true
            },
            { 
              path: constants.GRAVE_MANAGEMENT_CHILD_ROUTES.addBurial + '/:memorialLinkFlagProp/:addburialavailablePlotID?',
              name: constants.GRAVE_MANAGEMENT_CHILD_ROUTES.addBurial,
              component: AddBurial,
              props: true
            },
            { 
              path: constants.GRAVE_MANAGEMENT_CHILD_ROUTES.reservations + '/:personID?/:reservationavailablePlotID?',
              name: constants.GRAVE_MANAGEMENT_CHILD_ROUTES.reservations,
              component: DeathPersonDetails,
              props: true,
              children: [
                { 
                  path: constants.GRAVE_MANAGEMENT_CHILD_ROUTES.convertReservation,
                  name: constants.GRAVE_MANAGEMENT_CHILD_ROUTES.convertReservation,
                  component: ConvertReservation,
                  props: true
                },
                { 
                  path: constants.GRAVE_MANAGEMENT_CHILD_ROUTES.deleteReservation,
                  name: constants.GRAVE_MANAGEMENT_CHILD_ROUTES.deleteReservation,
                  component: DeleteReservation,
                  props: true
                }
              ]
            },
            { 
              path: constants.GRAVE_MANAGEMENT_CHILD_ROUTES.graveDetails,
              name: constants.GRAVE_MANAGEMENT_CHILD_ROUTES.graveDetails,
              component: GraveDetails,
              props: true
            },
            // { 
            //   path: constants.GRAVE_MANAGEMENT_CHILD_ROUTES.graveGeometry,
            //   name: constants.GRAVE_MANAGEMENT_CHILD_ROUTES.graveGeometry,
            //   component: FeatureGeometry,
            //   props: true
            // },
            { 
              path: constants.GRAVE_MANAGEMENT_CHILD_ROUTES.linkedMemorials + '/:linkedType/:showLabel',
              name: constants.GRAVE_MANAGEMENT_CHILD_ROUTES.linkedMemorials,
              component: LinkedMemorials,
              props: true
            },
            { 
              path: constants.GRAVE_MANAGEMENT_CHILD_ROUTES.graveOwnership + '/:deedID?/:ownershipavailablePlotID?',
              name: constants.GRAVE_MANAGEMENT_CHILD_ROUTES.graveOwnership,
              component: GraveOwnership,
              props: true,
              children: [
                { 
                  path: constants.GRAVE_MANAGEMENT_CHILD_ROUTES.graveowner + '/:ownerID/:startDay?/:startMonth?/:startYear?/:firstOwner?',
                  name: constants.GRAVE_MANAGEMENT_CHILD_ROUTES.graveowner,
                  component: GraveOwner,
                  props: true
                },
                { 
                  path: constants.GRAVE_MANAGEMENT_CHILD_ROUTES.newGraveOwner + '/:transfer/:startDay?/:startMonth?/:startYear?/:firstOwner?',
                  name: constants.GRAVE_MANAGEMENT_CHILD_ROUTES.newGraveOwner,
                  component: AddOwner,
                  props: true
                }
              ]
            },
            { 
              path: constants.GRAVE_MANAGEMENT_CHILD_ROUTES.attributes,
              name: constants.GRAVE_MANAGEMENT_CHILD_ROUTES.attributes,
              component: FeatureAttributes,
              props: true
            },
            { 
              path: constants.GRAVE_MANAGEMENT_CHILD_ROUTES.surveys + '/:surveyID?',
              name: constants.GRAVE_MANAGEMENT_CHILD_ROUTES.surveys,
              component: FeatureSurveys,
              props: true
            }
          ]
        }
      ]
    },
    {
      path: '/' + constants.MEMORIAL_MANAGEMENT_PATH + '/:id/:layer',
      name: constants.MEMORIAL_MANAGEMENT_PATH,
      component: MemorialManagement,
      children: [
        {
          path: 'o',
          name: 'memorialManagementContainer',
          component: ContentContainer,
          children: [
            { 
              path: constants.MEMORIAL_MANAGEMENT_CHILD_ROUTES.persons + '/:burial_id?/:person_id',
              name: constants.MEMORIAL_MANAGEMENT_CHILD_ROUTES.persons,
              component: PersonBurialDetails,
              props: true
            },
            { 
              path: constants.MEMORIAL_MANAGEMENT_CHILD_ROUTES.addPerson + '/:memorialLinkFlagProp',
              name: constants.MEMORIAL_MANAGEMENT_CHILD_ROUTES.addPerson,
              component: AddBurial,
              props: true
            },
            { 
              path: constants.MEMORIAL_MANAGEMENT_CHILD_ROUTES.memorialDetails,
              name: constants.MEMORIAL_MANAGEMENT_CHILD_ROUTES.memorialDetails,
              component: MemorialDetails,
              props: true
            },
            // { 
            //   path: constants.MEMORIAL_MANAGEMENT_CHILD_ROUTES.memorialGeometry,
            //   name: constants.MEMORIAL_MANAGEMENT_CHILD_ROUTES.memorialGeometry,
            //   component: FeatureGeometry,
            //   props: true
            // },
            { 
              path: constants.MEMORIAL_MANAGEMENT_CHILD_ROUTES.photos,
              name: constants.MEMORIAL_MANAGEMENT_CHILD_ROUTES.photos,
              component: Photos,
              props: true
            },
            { 
              path: constants.MEMORIAL_MANAGEMENT_CHILD_ROUTES.linkedGraves + '/:linkToGraveProp/:selectFlagProp/:showLabelProp',
              name: constants.MEMORIAL_MANAGEMENT_CHILD_ROUTES.linkedGraves,
              component: GraveLinkComponent,
              props: true
            },
            { 
              path: constants.MEMORIAL_MANAGEMENT_CHILD_ROUTES.attributes,
              name: constants.MEMORIAL_MANAGEMENT_CHILD_ROUTES.attributes,
              component: FeatureAttributes,
              props: true
            },
            { 
              path: constants.MEMORIAL_MANAGEMENT_CHILD_ROUTES.surveys + '/:surveyID?',
              name: constants.MEMORIAL_MANAGEMENT_CHILD_ROUTES.surveys,
              component: FeatureSurveys,
              props: true
            }
          ]
        }
      ]
    },
    {
      path: '/' + constants.BURIAL_PERSON_MANAGEMENT_PATH + '/:id',
      name: constants.BURIAL_PERSON_MANAGEMENT_PATH,
      component: BurialPersonManagement,
      children: [
        {
          path: 'o',
          name: 'burialpersonManagementContainer',
          component: ContentContainer,
          children: [
            { 
              path: constants.BURIAL_PERSON_MANAGEMENT_CHILD_ROUTES.person + '/:burial_id?/:person_id',
              name: constants.BURIAL_PERSON_MANAGEMENT_CHILD_ROUTES.person,
              component: PersonBurialDetails,
              props: true
            }
          ]
        }
      ]
    },
    {
      path: '/' + constants.PERSON_MANAGEMENT_PATH + '/:id',
      name: constants.PERSON_MANAGEMENT_PATH,
      component: PersonManagement,
      children: [
        {
          path: 'o',
          name: 'personManagementContainer',
          component: ContentContainer,
          children: [
            { 
              path: constants.PERSON_MANAGEMENT_CHILD_ROUTES.persondetails,
              name: constants.PERSON_MANAGEMENT_CHILD_ROUTES.persondetails,
              component: PersonDetails,
              props: true,
              children: [
                { 
                  path: constants.PERSON_MANAGEMENT_CHILD_ROUTES.persondetailsaddress + '/:addressID?/:createNew?',
                  name: constants.PERSON_MANAGEMENT_CHILD_ROUTES.persondetailsaddress,
                  component: Address,
                  props: true,
                }
              ]
            },
            { 
              path: constants.PERSON_MANAGEMENT_CHILD_ROUTES.personownership,
              name: constants.PERSON_MANAGEMENT_CHILD_ROUTES.personownership,
              component: PersonCompanyOwnership,
              props: true
            },
            { 
              path: constants.PERSON_MANAGEMENT_CHILD_ROUTES.personNextOfKinTo,
              name: constants.PERSON_MANAGEMENT_CHILD_ROUTES.personNextOfKinTo,
              component: PersonNextOfKinTo,
              props: true
            }
          ]
        }
      ]
    },
    {
      path: '/' + constants.COMPANY_MANAGEMENT_PATH + '/:id',
      name: constants.COMPANY_MANAGEMENT_PATH,
      component: CompanyManagement,
      children: [
        {
          path: 'o',
          name: 'companyManagementContainer',
          component: ContentContainer,
          children: [
            { 
              path: constants.COMPANY_MANAGEMENT_CHILD_ROUTES.companydetails,
              name: constants.COMPANY_MANAGEMENT_CHILD_ROUTES.companydetails,
              component: CompanyDetails,
              props: true,
              children: [
                { 
                  path: constants.COMPANY_MANAGEMENT_CHILD_ROUTES.companydetailsaddress + '/:addressID?/:createNew?',
                  name: constants.COMPANY_MANAGEMENT_CHILD_ROUTES.companydetailsaddress,
                  component: Address,
                  props: true,
                }
              ]
            },
            { 
              path: constants.COMPANY_MANAGEMENT_CHILD_ROUTES.companyownership,
              name: constants.COMPANY_MANAGEMENT_CHILD_ROUTES.companyownership,
              component: PersonCompanyOwnership,
              props: true
            }
          ]
        }
      ]
    },
    {
      path: '/' + constants.FEATURE_MANAGEMENT_PATH + '/:id/:layer',
      name: constants.FEATURE_MANAGEMENT_PATH,
      component: FeatureManagement,
      props: true,
      children: [
        {
          path: 'o',
          name: 'featureManagementContainer',
          component: ContentContainer,
          children: [
            { 
              path: constants.FEATURE_MANAGEMENT_CHILD_ROUTES.attributes,
              name: constants.FEATURE_MANAGEMENT_CHILD_ROUTES.attributes,
              component: FeatureAttributes,
              props: true
            },
            { 
              path: constants.FEATURE_MANAGEMENT_CHILD_ROUTES.surveys + '/:surveyID?',
              name: constants.FEATURE_MANAGEMENT_CHILD_ROUTES.surveys,
              component: FeatureSurveys,
              props: true
            }
          ]
        }
      ]
    }
  ]
});

/**
 * Vue Router navigation guard: called before navigation
 */
router.beforeEach((to, from, next) => {

  // true if a new management tool has been selected (i.e. grave management or memorial management) 
  const managementToolChanged = to.params.id !== from.params.id;
  // true if a different section has been selected
  const sectionChanged = !managementToolChanged && to.name !== from.name;

  if (store.state.ManagementTool.closeFlag || managementToolChanged) {

    // remove highlighting overlay if closing/changing tool
    let personInteractionService = store.getters.personInteractionService;
    if (personInteractionService && personInteractionService.featureOverlays['hightlighted-features'])
      personInteractionService.featureOverlays['hightlighted-features'].removeAllFeatures();
  }

  if (managementToolChanged)
    featureSidebarStore.actions.resetFeatureData(store);

  if (managementToolChanged || sectionChanged) 
    updateHistory(to);

  moveToNext(to, from, next);
});

/**
 * Moves to next url. Timeout is used if closing to allow for the sliding animations.
 */
function moveToNext(to, from, next) {

  store.commit('goBackFlag', false);
  store.commit('goForwardFlag', false);
  store.commit('closeFlag', false);

  if (store.state.ManagementTool.closeFlag) {
    // allow time for animations
    setTimeout(() => {
      next();
    }, 300);
  }
  else
    next();
}

/**
 * Updates history states in vuex (used in nav buttons at top of management tool)
 */
function updateHistory(to) {
 
  if (store.state.ManagementTool.goBackFlag)
    store.commit('goBack');
  else if (store.state.ManagementTool.goForwardFlag)
    store.commit('goForward');
  else {
    store.commit('routerChange', to);
  
    if (store.state.ManagementTool.closeFlag) {
      
      store.commit('setManagementToolOpen', false);
      
      // set right
      document.getElementById('management-tool-contentbar-container').style.right = - mapManagementConstants.TOOL_CONTENT_WIDTH - mapManagementConstants.TOOL_BORDER_WIDTH - 5 + "px";
      document.getElementById('management-tool-container').style.right = - mapManagementConstants.TOOL_WIDTH - 5 + "px";
      
      // set layers accordion position
      let layersAccordion = document.getElementById('layersAccordion');
      if (layersAccordion) {
        layersAccordion.style.right = "5px";
        layersAccordion.style.top = "100px";
      }
      
      // display tools accordion
      let horizontalToolsAccordion = document.getElementById('horizontalToolsAccordion');
      if (horizontalToolsAccordion)
        horizontalToolsAccordion.style.display = "inline-flex";

      store.commit('resetHistory');
    }
    else
      store.commit('setManagementToolOpen', true);
  }
}

export default router;