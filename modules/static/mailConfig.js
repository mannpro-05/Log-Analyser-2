$(document).ready(function () {
    $('.menu-toggle').click(function () {
      $('.menu-toggle').toggleClass('active')
      $('nav').toggleClass('active')
    });
    // $('#MailConfigSendBtn').click(validateInput());
  })

  


function mailConfig(){

    var data = {
        "MAIL_PORT" : $("#mailPort").val(),
        "MAIL_SERVER" : $("#mailServer").val(),
        "MAIL_USERNAME" : $("#mailUsername").val(),
        "MAIL_PASSWORD" : $("#password").val(),
        "MAIL_USE_SSL" : $("#ssl").val()
    }
    console.log(data)
     $.ajax({
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(data),
        dataType: 'json',
        url: '/mailConfig'

    }).done(function (data) {
        alert(data.message);
        location.reload();
    })
}





  
  function validateInput(){
    let userSMTP_SERVER=document.getElementById("mailServer");
    let userMAIL_PORT=document.getElementById("mailPort");
    let email=document.getElementById("mailUsername");
    let pwd=document.getElementById("password");
    let form=document.querySelector("form");
    //check username is empty
      if(userSMTP_SERVER.value.trim()===""){
        onError(userSMTP_SERVER,"SMTP_SERVER cannot be empty");
        userSMTP_SERVER.focus();
        return false;
         
      }else{
          onSuccess(userSMTP_SERVER);
      }
  
      if(userMAIL_PORT.value.trim()===""){
         onError(userMAIL_PORT,"MAIL_PORT cannot be empty");
         userMAIL_PORT.focus();
         return false;
         
      }else{
          onSuccess(userMAIL_PORT);
      }
      if(email.value.trim()===""){
          onError(email,"Email cannot be empty");
          email.focus()
          return false;
      }else{
          if(!isValidEmail(email.value.trim())){
              onError(email,"Email is not valid");
              email.focus();
              return false;
          }else{
              onSuccess(email);
          }
      }
  
      //password
      if(pwd.value.trim()===""){
          onError(pwd,"Password Field Cannot Be Empty");
          pwd.focus();
          return false;
       }else{
           onSuccess(pwd);
       }
       return true;
  }
  
//   document.querySelector("button")
//   .addEventListener("click",(event)=>{
//       event.preventDefault();
//       validateInput();
//   });
  
  function onSuccess(input){
      let parent=input.parentElement;
      let messageEle=parent.querySelector("small");
      messageEle.style.visibility="hidden"; 
      parent.classList.remove("error");
      parent.classList.add("success");  
  }
  function onError(input,message){
      let parent=input.parentElement;
      let messageEle=parent.querySelector("small");
      messageEle.style.visibility="visible";
      messageEle.innerText=message;  
      parent.classList.add("error");
      parent.classList.remove("success");
  
  }
  
  function isValidEmail(email){
     return /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/.test(email);
  }
  
  