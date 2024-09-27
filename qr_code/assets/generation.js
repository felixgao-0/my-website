let qrImage = 0;
const imageOptions = {
    0: null, // Nothing ):
    1: "assets/flag-standalone.png",
    2: "assets/flag-orpheus-left.png",
    3: "assets/flag-orpheus-top.png",
    4: "assets/flag-standalone-bw.png",
    5: "assets/flag-orpheus-left-bw.png",
    6: "assets/flag-orpheus-top-bw.png",
    7: "assets/icon-progress-rounded.png",
    8: "assets/icon-rounded.png"
}
let qrCode = null;
/*
function setQRImage(number) {
    const buttons = document.querySelectorAll('.gallery button');

    buttons.forEach(button => {
        button.classList.remove('selected');
    });

    buttons[number].classList.add('selected');

    qrImage = imageOptions[number];
}*/

function generateQRCode() {
    document.getElementById("qr-code").innerHTML = ''; // Clear any left over QR codes
    let errorCorLv = document.getElementById('error-correction').value;
    console.log(errorCorLv);

    // Show the download btns :)
    const div = document.querySelector('.download');

    const buttons = div.querySelectorAll('button');

    buttons.forEach(button => {
        button.classList.remove('hidden');
    });

    qrCode = new QRCodeStyling({
        type: "svg",
        data: document.getElementById("url-field").value,
        qrOptions: {
            errorCorrectionLevel: errorCorLv
        }
    });

    qrCode.append(document.getElementById("qr-code"));
}

function downloadQRCode(type) {
    qrCode.download(type)
}