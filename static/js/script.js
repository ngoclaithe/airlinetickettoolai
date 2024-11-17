document.getElementById('downloadAllButton').style.display = 'block';

function handleSubmit() {

    document.querySelector('.print-btn').style.display = 'none';
    return true;
}
function showPrintButton() {
    const printButton = document.querySelector('.print-btn');
    if (printButton) {
        printButton.style.display = 'block';
    }
}

function downloadPDF(passengerName) {
    const selectedItems = getSelectedCheckboxes();

    const xhr = new XMLHttpRequest();
    xhr.open("POST", "/download_pdf", true);
    xhr.setRequestHeader("Content-Type", "application/json");

    xhr.onload = function () {
        if (xhr.status === 200) {
            const contentDisposition = xhr.getResponseHeader('Content-Disposition');
            let filename = 'download.pdf';

            if (contentDisposition && contentDisposition.indexOf('filename=') !== -1) {
                const matches = /filename[^;=\n]*=((['"]).*?\2|([^;\n]*))/;
                const parts = matches.exec(contentDisposition);
                if (parts && parts[1]) {
                    filename = parts[1].replace(/['"]/g, '');
                }
            }

            const blob = new Blob([xhr.response], { type: 'application/pdf' });
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = filename;

            document.body.appendChild(a);
            a.click();
            a.remove();
            window.URL.revokeObjectURL(url);
        } else {
            console.error('Failed to download PDF:', xhr.responseText);
        }
    };

    xhr.onerror = function () {
        console.error('Request failed');
    };

    xhr.responseType = 'blob';
    xhr.send(JSON.stringify({ 
        passenger_name: passengerName,
        selected_fields: selectedItems 
    }));
}
function downloadAllPDF() {
    const selectedItems = getSelectedCheckboxes();
    
    const xhr = new XMLHttpRequest();
    xhr.open("POST", "/download_all_pdf", true);
    xhr.setRequestHeader("Content-Type", "application/json");

    xhr.onload = function () {
        if (xhr.status === 200) {
            const blob = new Blob([xhr.response], { type: 'application/zip' });
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'all_tickets.zip'; 

            document.body.appendChild(a);
            a.click();
            a.remove();
            window.URL.revokeObjectURL(url);
        } else {
            console.error('Failed to download all PDFs:', xhr.responseText);
        }
    };

    xhr.onerror = function () {
        console.error('Request failed');
    };

    xhr.responseType = 'blob';
    xhr.send(JSON.stringify({ 
        selected_fields: selectedItems 
    }));
}

function getSelectedCheckboxes() {
    const checkboxes = document.querySelectorAll(".select-checkbox");
    const selectedItems = [];
    
    checkboxes.forEach((checkbox) => {
        if (checkbox.checked) {
            selectedItems.push(checkbox.value);
        }
    });
    
    return selectedItems;
}

document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("downloadAllButton").addEventListener("click", function() {
        downloadAllPDF();
    });
});
document.getElementById('bookingData').addEventListener('input', function() {
    localStorage.setItem('bookingData', this.value);
});
window.onload = function() {
    if (localStorage.getItem('bookingData')) {
        document.getElementById('bookingData').value = localStorage.getItem('bookingData');
    }
}