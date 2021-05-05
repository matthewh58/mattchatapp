function login(){
    var username = $("#username").val()
    var password = $("#password").val()


    $.ajax({

      type: "POST",
      url: "/loginrequest",
      data: {"username": username, "password": password},
      success: function(response){
           if (response == "yay"){
                window.location.href = "/home"
           }
           else{
                $("#error").text(response)
           }
      }
    });
}

function verify(){
    var passcode = $("#passcode").val()

    $.ajax({

      type: "POST",
      url: "/verifyrequest",
      data: {"passcode": passcode},
      success: function(response){
           if (response == "yay"){
                window.location.href = "/home"
           }
           else{
                $("#error").text(response)
           }
      }
    });
}

function register(){
    var username = $("#username").val()
    var password = $("#password").val()
    var confirmPassword = $("#confirmPassword").val()
    var email = $("#email").val()


    $.ajax({

      type: "POST",
      url: "/registerrequest",
      data: {"username": username, "password": password, "confirmPassword": confirmPassword, "email": email},
      success: function(response){
           if (response == "yay"){
                window.location.href = "/verify"
           }
           else{
                $("#error").text(response)
           }
      }
    });
}

function friends(){
    $("#people").show()
    $("#groups").hide()
    $("#friendicon").css("background", "white")
    $("#groupicon").css("background", "#00000000")
}

function groups(){
    $("#groups").show()
    $("#people").hide()
    $("#groupicon").css("background", "white")
    $("#friendicon").css("background", "#00000000")
}

function settings(){


    $.ajax({
      type: "POST",
      url: "/settings",
      data: {"username": username, "email": email, "image": image},
      success: function(response){
           if (response == "yay"){
                window.location.href = "/settings"
           }
           else{
                $("#error").text(response)
           }
      }
    });
}

function messages(other, isGroup){
    var message = $("#message").val()

    $.ajax({
      type: "POST",
      url: "/message",
      data: {"user2": other, "message": message, "isGroup": isGroup},
      success: function(response){
           if (response == "yay"){
                window.location.reload()
           }
           else{
                $("#error").text(response)
           }
      }
    });
}

function createGroup(){
    var image = $("#groupImage").val()
    var name = $("#groupName").val()
    var description = $("#groupDescription").val()

    $.ajax({
      type: "POST",
      url: "/creategroup",
      data: {"groupName": name, "groupImage": image, "groupDescription": description},
      success: function(response){
           if (response == "yay"){
                window.location.href = "/home"
           }
           else{
                $("#error").text(response)
           }
      }
    });
}

function changeUser(){
    var image = $("#newImage").val()
    var username = $("#newUsername").val()
    var oldPassword = $("#oldPass").val()
    var newPassword = $("#newPass").val()

    $.ajax({
      type: "POST",
      url: "/updateUser",
      data: {"image": image, "username": username, "oldPassword": oldPassword, "newPassword": newPassword},
      success: function(response){
           if (response == "yay"){
                window.location.reload()
           }
           else{
                $("#error").text(response)
           }
      }
    });
}

