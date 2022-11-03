/**
 * Messages config file for the client side app
 */

var baseMessages = {
  confirmation: {
    title: "Confirmation Needed",
  },
};

 /**
  * Divided by modules/parts of the app, define notification and include title,text.
  * @module messages
  */
var messages = {
  /** Notifications for burial information form */
	burialDetails: {
    saveChanges: {
      confirmation: {
        title: baseMessages.confirmation.title,
        text: "Do you want to save your changes?",
      },
      hasErrors: {
        title: "Update Unsuccessful",
        text: "Please correct the form errors first",
      },
      isEmptyForm: {
        title: "Update Unsuccessful",
        text: "Please complete at least one field in Person Details and Burial Record Details forms",
      },
      success: {
        title: "Update Successful",
      },
      fail: {
        title: "Update Unsuccessful",
      },
    },
    getAllBurialOfficials: {
      error: {
          title: "Error loading burial officials",
      },
    },
    validateClosingModal: {
      title: "Action Required",
      text: "Please save or discard changes first",
    },
    fileUpload: {
      validationFileType: {
        title: "Please select jpeg or png image file type only",
      },
      validationFileSize: {
        title: "Please upload a smaller image, max size is 5 MB",
      },
      success: {
        title: "Update Successful",
      },
      fail: {
        title: "Update Unsuccessful",
      }
    },
  },
  toolbar: {
    toggleOption: {
      title: baseMessages.confirmation.title,
      text: "Do you want to stop creating the plot?",
    },
    memorial: {
      delete: {
        confirmation: {
          title: baseMessages.confirmation.title,
          text: "Do you want to delete the memorial?",
        },
        fail: {
          title: "The memorial could not be deleted.",
        },
        attatchedPersonFail: {
          title: "The memorial cannot be deleted whilst linked to a person."
        },
        success: {
          title: "The memorial was successfully deleted.",
        },
      },
      cancel: {
        confirmation: {
          title: baseMessages.confirmation.title,
          text: "Do you want to save changes to memorial?",
          textForNew: "Do you want to save the memorial?",
        },
      },
      save: {
        success: {
          title: "The memorial was successfully saved.",
        },
        fail: {
          title: "The memorial could not be saved.",
        },
      },
      confirmationAfterSuccess: {
        title: baseMessages.confirmation.title,
        text: "Do you want to link a plot to this memorial?",
      },
      capture: {
        title: 'Click a memorial to capture data',
        text: '<i class="fa fa-times" aria-hidden="true"></i> indicates a memorial which has no image!',
      },
    },
    plot: {
      linkMemorial: {
        confirmation: {
          title: baseMessages.confirmation.title,
          text: "Are you sure you want to link the memorial to this plot?",
        },
        success: {
          title: "The memorial was successfully linked to the plot.",
        },
        fail: {
          title: "The memorial could not be linked to the plot selected.",
        },
        error: {
          title: "Please add burial details to the plot before linking.",
        },
      },
      linkGraveRef: {
        confirmation: {
          title: baseMessages.confirmation.title,
          text: "Any information linked to the existing grave number will be removed. If you have entered a new grave number, these details will be linked instead \n Are you sure you want to continue?",
        }
      },
      delete: {
        confirmation: {
          title: baseMessages.confirmation.title,
          text: "Do you want to delete the plot?",
        },
        fail: {
          title: "The plot could not be deleted.",
        },
        success: {
          title: "The plot was successfully deleted.",
        },
      },
      cancel: {
        confirmation: {
          title: baseMessages.confirmation.title,
          text: "Do you want to save changes to the plot?",
        },
      },
      save: {
        success: {
          title: "The plot was successfully saved.",
        },
        fail: {
          title: "The plot could not be saved.",
        },
      },
    },
  },
  search: {
    unknowLocation: {
      title: "Unknown location",
    },
  },
  memorialImages: {
    delete: {
      confirmation: {
        title: baseMessages.confirmation.title,
        text: "Do you want to delete the photo?",
      },
      fail: {
        title: "The photo could not be deleted.",
      },
      success: {
        title: "The photo was successfully deleted.",
      },
    },
    upload: {
      success: {
        title: "The photo was uploaded successfully.",
      },
      fail: {
        title: "The photo could not be uploaded.",
      }
    }
  },
  buryPerson: {
    confirmation: {
      text: "Are you sure you want to convert this reservation to a burial?",
    },
    cancel: {
      text: "Are you sure you want to close the form?",
    },
    cancelReservedPerson: {
      text: "Are you sure you want to cancel this reservation?",
      error: "Update Unsuccessful",
      success: "Update Successful",
    },
  },
  inspection: {
    save: {
      success: {
        title: "Inspection added"
      },
      fail: {
        title: "Unable to add inspection"
      },
    },
  },
  memorialInscriptions: {
    save: {
      success: {
        title: "Memorial inscription added"
      },
      fail: {
        title: "Unable to add memorial inscription"
      },
    },
    delete: {
      success: {
        title: "Memorial inscription deleted"
      },
      fail: {
        title: "Unable to delete memorial inscription"
      },
    },
  },
};