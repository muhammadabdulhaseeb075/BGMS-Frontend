/** @module
 *  Admin site portal Data Upload Tool
 */

axios.defaults.headers.common["X-CSRFToken"] = document.getElementsByName('csrfmiddlewaretoken')[0].value;

function linkBurialRegisters() {
	$("body").css("cursor", "progress");
	axios({
		method: 'post',
		url: "linkRegisters/",
    data: { burial_register: true }
  })
  .then(function (response) {
		let count = response.data.count;
		$("body").css("cursor", "default");
		notificationService.successSticky('Linking burial records to registers was successful. ' + count + ' links created.');
  })
  .catch(function (error) {
		$("body").css("cursor", "default");
		notificationService.errorSticky('Linking burial records to registers failed.');
    console.error(error);
  });
}

function linkOwnershipRegisters() {
	$("body").css("cursor", "progress");
	axios({
		method: 'post',
    url: "linkRegisters/",
    data: { ownership_register: true }
  })
  .then(function (response) {
		let count = response.data.count;
		$("body").css("cursor", "default");
		notificationService.successSticky('Linking ownership records to registers was successful. ' + count + ' links created.');
  })
  .catch(function (error) {
		$("body").css("cursor", "default");
		notificationService.errorSticky('Linking ownership records to registers failed.');
    console.error(error);
  });
}

function updateGraveplotLayers() {
	$("body").css("cursor", "progress");
	axios({
		method: 'get',
		url: "updateGraveplotLayers/",
  })
  .then(function (response) {
		let data = response.data;
    $("body").css("cursor", "default");
    let message = '';

    // report on what records were changed.
    if (data.plot_to_reserved_plot_count || data.plot_to_available_plot_count || data.reserved_plot_to_plot_count || data.reserved_plot_to_available_plot_count || data.available_plot_to_plot_count || data.available_plot_to_reserved_plot_count) {

      if (data.plot_to_reserved_plot_count)
        message += `${data.plot_to_reserved_plot_count} ${data.plot_to_reserved_plot_count>1 ? 'records' : 'record'} changed from plot to reserved plot.\n`;
      if (data.plot_to_available_plot_count)
        message += `${data.plot_to_available_plot_count} ${data.plot_to_available_plot_count>1 ? 'records' : 'record'} changed from plot to available plot.\n`;
      if (data.reserved_plot_to_plot_count)
        message += `${data.reserved_plot_to_plot_count} ${data.reserved_plot_to_plot_count>1 ? 'records' : 'record'} changed from reserved plot to plot.\n`;
      if (data.reserved_plot_to_available_plot_count)
        message += `${data.reserved_plot_to_available_plot_count} ${data.reserved_plot_to_available_plot_count>1 ? 'records' : 'record'} changed from reserved plot to available plot.\n`;
      if (data.available_plot_to_plot_count)
        message += `${data.available_plot_to_plot_count} ${data.available_plot_to_plot_count>1 ? 'records' : 'record'} changed from available plot to plot.\n`;
      if (data.available_plot_to_reserved_plot_count)
        message += `${data.available_plot_to_reserved_plot_count} ${data.available_plot_to_reserved_plot_count>1 ? 'records' : 'record'} changed from available plot to reserved plot.`;
    }
    else
      message += "No records were changed.";


		notificationService.successStickyTitleAndMessage('Updating graveplot layers was successful.', message);
  })
  .catch(function (error) {
		$("body").css("cursor", "default");
		notificationService.errorSticky('Updating graveplot layers failed.');
    console.error(error);
  });
}

async function beginDataUpload() {

	let burialFile = getFilefromInputControl('#id_burial_csv_file')
	if (burialFile === false)
		return;
	
	let graveFile = getFilefromInputControl('#id_grave_csv_file')
	if (graveFile === false)
		return;
	
	let graveOwnershipFile = getFilefromInputControl('#id_grave_ownership_csv_file')
	if (graveOwnershipFile === false)
		return;
	
		let relationFile = getFilefromInputControl('#id_relations_csv_file')
		if (relationFile === false)
			return;
	
	if (!burialFile && !graveFile && !graveOwnershipFile && !relationFile) {
		notificationService.errorSticky('You must include at least one csv file!');
		return;
	}

	let formData=new FormData();

	if (graveFile) {
		if (await validateFileHeaders(graveFile, "grave", validGraveHeaders)) {
			formData.append("graveFile",graveFile);
		}
		else
			return;
	}

	if (graveOwnershipFile) {
		if (await validateFileHeaders(graveOwnershipFile, "graveOwners", validGraveOwnersHeaders)) {
			formData.append("graveOwnershipFile",graveOwnershipFile);
		}
		else
			return;
	}

	if (burialFile) {
		if (await validateFileHeaders(burialFile, "burial", validBurialHeaders)) {
			formData.append("burialFile",burialFile);
		}
		else
			return;
	}

	if (relationFile) {
		if (await validateFileHeaders(relationFile, "relation", validRelationsHeaders)) {
			formData.append("relationFile",relationFile);
		}
		else
			return;
	}

		// validation successful so upload file to server
		uploadCSVFile(formData);
}

// upload csv files to server and begin to add to db
function uploadCSVFile(formData) {
	axios({
		method: 'post',
		url: "submitDataUpload/",
		data: formData,
		headers: {
			'Content-Type': 'multipart/form-data'
		},
  })
  .then(function (response) {
    console.log(response);

    let data = response.data;

		// update table to show this upload
    $("#previousdataUploadsTable tbody").prepend("<tr id='" + data.dataUploadRecordID + "'><td>" + data.fileName + "</td><td>" + moment(data.date).format('D MMM YYYY') + "</td><td></td><td>Processing</td></tr>");
  })
  .catch(function (error) {
    console.log(error);
  });
}

function refreshPage() {
	window.location.reload(true);
}

// delete all the data that was added during a data upload
function deleteDataUpload(id, recordCount, filename) {
	if (confirm("Warning! This will delete all records (" + recordCount + ") added from '" + filename +"'. Are you sure you want to continue?")) {
		if (confirm("Warning! This cannot be undone. Are you certain you want to continue?")) {
			let temp = axios.defaults;
			axios({
				method: 'post',
				url: 'deleteDataUpload/',
				data: {'id': id}
			})
		  .then(function () {
				// update table to show this upload
		    $("#status_" + id)[0].innerHTML = "Deleting";
		    $("#delete_icon_" + id)[0].innerHTML = "";
		  })
		  .catch(function (error) {
		    console.log(error);
		  });
		}
	}
}

function getFilefromInputControl(fileInputControlID) {

	let file = $(fileInputControlID)[0].files[0];

	if (file) {
		// check the the file is actually a CSV file
		fileExtension = file.name.substr((file.name.lastIndexOf('.') + 1));

		if (fileExtension !== "csv") {
			$(fileInputControlID)[0].value = null;
			notificationService.errorSticky('The file must be a CSV file.');
			return false;
		}
	}

	return file;
}

const validateFileHeaders = (file, type, validHeaders) => {
	// get the csv headers
	let reader = new FileReader();
	reader.readAsArrayBuffer(file);
	return new Promise((resolve, reject) => {
		reader.onloadend = function (evt) {

			let data = evt.target.result;
			let byteLength = data.byteLength;

			if (byteLength === 0) {
				notificationService.errorSticky('The CSV file you have selected is empty!');
				resolve(false);
			}

			// Convert to conventional array, so we can iterate though it
			let ui8a = new Uint8Array(data, 0);

			// Used to store each character that makes up CSV header
			let headerString = '';

			// Iterate through each character in our Array
			for (let i = 0; i < byteLength; i++) {
				// Get the character for the current iteration
				var char = String.fromCharCode(ui8a[i]);

				// Check if the char is a new line
				if (char.match(/[^\r\n]+/g) !== null) {

					// Not a new line so lets append it to our header string and keep processing
					headerString += char;
				} else {
					// We found a new line character, stop processing
					break;
				}
			}

			// Split our header string into an array
			let headers = headerString.split(',');

			let fullName;

			// validate the csv headers
			for (let j=0;j<headers.length;j++) {
			// look out for unrecognised headers
				if (validHeaders.indexOf(headers[j]) === -1) {
					if (!confirm("The header '" + headers[j] + "' in your CSV file is not recognised by BGMS and will be ignored. Do you want to continue?"))
						return resolve(false);
				}

				// Validation specific to burial data
				if (type === "burial" || type === "graveOwners") {
					// look out for incompatible name fields
					if (((headers[j] === "first_names" || headers[j] === "last_name") && fullName)
							|| (headers[j] === 'full_name' && fullName === false)) {
						notificationService.errorSticky("The CSV file can contain the fields 'first_names' and 'last_name' OR the field 'full_name'.");
						return resolve(false);
					}
					else if (headers[j] === "first_names" || headers[j] === "last_name")
						fullName = false;
					else if (headers[j] === 'full_name') {
						fullName = true;

						// ask the user for permission to break down 'full_name'
						if (!confirm("Your CSV file contains the header 'full_name'. BGMS will automatically split up this column by putting the last name into 'last_name' and any preceeding names into 'first_names'. Do you want to continue?"))
							return resolve(false);
					}
				}
			}

			resolve(true);
		}
	});
}
