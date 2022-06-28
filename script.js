var op = "";



function startDictation() {
    if (window.hasOwnProperty('webkitSpeechRecognition')) {
        var recognition = new webkitSpeechRecognition();

        recognition.continuous = false;
        recognition.interimResults = false;

        recognition.lang = 'en-US';
        recognition.start();

        recognition.onresult = function (e) {
            ip = e.results[0][0].transcript;
        };

        recognition.onerror = function (e) {
            recognition.stop();
        };
    }
    $(".chats").append("<div id=\"a\">" + ip + "</div>");

    $(".chats > #a").addClass("my-chat");

    op = getString(ip);

    f2(op);

    $(".chats").append("<div id = \"b\">" + op + "</div>");

    $(".chats > #b").addClass("client-chat");
}

$(document).ready(function(){
    $("#sub").click(function(){
        var str = $("#inp").val();
        $("#inp").val("");
            $(".chats").append("<div id=\"a\">"+str+"</div>");
            $(".chats > #a").addClass("my-chat");
            op = getString(str);
            f2(op);
            $(".chats").append("<div id = \"b\">"+op+"</div>");
            $(".chats > #b").addClass("client-chat");
    });

    $("#inp").keypress(function(e){
        if(e.which === 13){
            var str = $("#inp").val();
            $("#inp").val("");
            $(".chats").append("<div id=\"a\">"+str+"</div>");
            $(".chats > #a").addClass("my-chat");
            op = getString(str);
            f2(op);
            $(".chats").append("<div id = \"b\">"+op+"</div>");
            $(".chats > #b").addClass("client-chat");
        }
    });

    $(".mic-icon").click(function(){
        startDictation();
        $(".outline").css("animation","pulse 3s ease-out infinite");
    })
});

function getString(inp){
    /*const request = new XMLHttpRequest();
    request.open('POST','/index/${JSON.stringify(inp)}');
    request.send();*/
    $.ajax({
        url: "/index",
        type: "POST",
        contentType: "application/json"
        data: JSON.stringify(inp)   // converts js value to JSON string
    });
    var res='';
    //var res={{result}};
    return res;
}



function f2(x) {
    $(".outline1").css("animation","pulse 3s ease-out infinite");
    var voices = window.speechSynthesis.getVoices();
    var msg = new SpeechSynthesisUtterance();
    msg.voice = voices[8]; 
    msg.text = x;
    window.speechSynthesis.speak(msg);
    $(".outline1").css("animation","pulse 0s ease-out infinite");
}

