window.addEventListener("load", function () {
    var video = document.getElementById("vid-show"),
        canvas = document.getElementById("vid-canvas"),
        take = document.getElementById("vid-take");

    navigator.mediaDevices.getUserMedia({video: true})
        .then(function (stream) {

            video.srcObject = stream;
            video.play();

            take.addEventListener("click", function () {
                // Create snapshot from video
                var draw = document.createElement("canvas");
                draw.width = video.videoWidth;
                draw.height = video.videoHeight;
                var context2D = draw.getContext("2d");
                context2D.drawImage(video, 0, 0, video.videoWidth, video.videoHeight);
                // console.write(draw.toDataURL());

                var imageBase64Data = draw.toDataURL('image/jpeg', 1.0);
                var xhr = new XMLHttpRequest();
                xhr.open('POST', "/onClick", true);
                xhr.setRequestHeader("Content-Type", "application/json");


                xhr.onload = function () {
                    if (xhr.status == 403 || xhr.status == 404) {
                        alert("ERROR LOADING /onClick python service");
                    } else {
                        // alert(this.response);

                        let out = document.getElementById('out');
                        while (out.firstChild) {
                            out.removeChild(out.firstChild);
                        }
                        let inpResponse = this.response;
                        inpResponse = JSON.parse(inpResponse);
                        // alert(inpResponse.accountId);
                        if (inpResponse.error != null) {
                            out.appendChild(document.createTextNode('Unknown Customer'));
                            out.appendChild(document.createElement("br"));
                        }

                        out.appendChild(document.createTextNode('Name :  ' + inpResponse.response.name));
                        out.appendChild(document.createElement("br"));
                        out.appendChild(document.createTextNode('AccountId : ' + inpResponse.response.accountId));
                        out.appendChild(document.createElement("br"));
                        out.appendChild(document.createTextNode('AccountType : ' + inpResponse.response.accountType));
                        out.appendChild(document.createElement("br"));
                        out.appendChild(document.createTextNode('Balance : ' + inpResponse.response.balance));
                        out.appendChild(document.createElement("br"));
                        out.appendChild(document.createTextNode('Branch : ' + inpResponse.response.mainBranch));
                        out.appendChild(document.createElement("br"));


                    }
                };
                xhr.send(imageBase64Data);


                // draw.toDataURL(function ('image/jpeg', 1.0) {
                //     // var data = new FormData();
                //     var xhr = new XMLHttpRequest();
                //     xhr.open('POST', "/onClick", true);
                //     xhr.setRequestHeader("Content-Type", "application/json");
                //
                //
                //     xhr.onload = function () {
                //         if (xhr.status == 403 || xhr.status == 404) {
                //             alert("ERROR LOADING /onClick python service");
                //         } else {
                //             alert(this.response);
                //         }
                //     };
                //     var data = data;
                //
                //     xhr.send(data);
                //
                // });

                //Upload to server
                // draw.toBlob(function (blob) {
                //     //var data = new FormData();
                //     //data.append('upimage', blob);
                //     var xhr = new XMLHttpRequest();
                //     xhr.open('POST', "/onClick", true);
                //     xhr.setRequestHeader("Content-Type", "application/json");
                //
                //
                //     xhr.onload = function () {
                //         if (xhr.status == 403 || xhr.status == 404) {
                //             alert("ERROR LOADING /onClick python service");
                //         } else {
                //             alert(this.response);
                //         }
                //     };
                //     // var data = blob;
                //     var reader = new FileReader();
                //     var stringdata = reader.readAsArrayBuffer(blob);
                //     var data = btoa(blob);
                //     // var base64String = reader.result;
                //     // var data = base64String;
                //
                //
                //     // var data = btoa(encodeURIComponent(blob.toString()).replace(/%([0-9A-F]{2})/g,
                //     //       function toSolidBytes(match, p1) {
                //     //           return String.fromCharCode('0x' + p1);
                //     // }));
                //
                //     // var data = btoa(blob)
                //
                //
                //     xhr.send(data);
                //
                // });
            });
        })
        .catch(function (err) {
            document.getElementById("vid-controls").innerHTML = "Please enable access and attach a camera";
        });
});