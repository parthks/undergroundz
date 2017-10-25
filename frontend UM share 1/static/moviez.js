function onSignIn(googleUser) {
  var profile = googleUser.getBasicProfile();
  console.log('ID: ' + profile.getId()); // Do not send to your backend! Use an ID token instead.
  console.log('Name: ' + profile.getName());
  console.log('Image URL: ' + profile.getImageUrl());
  console.log('Email: ' + profile.getEmail()); // This is null if the 'email' scope is not present.
  user_email = profile.getEmail()
}

user_email = 'blank'


$( document ).ready(function() {
    $('#search').click(function(){
        console.log('hiiii');
        console.log(user_email);
        var movieName = $('#movieName').val();
        alert('hi');
        console.log(movieName);



        var form = document.createElement("form");
        form.setAttribute("method", 'post');
        form.setAttribute("action", '/res');

            
        var hiddenField1 = document.createElement("input");
        hiddenField1.setAttribute("type", "hidden");
        hiddenField1.setAttribute("name", 'email');
        hiddenField1.setAttribute("value", user_email);

        form.appendChild(hiddenField1);

        var hiddenField2 = document.createElement("input");
        hiddenField2.setAttribute("type", "hidden");
        hiddenField2.setAttribute("name", 'movie');
        hiddenField2.setAttribute("value", movieName);

        form.appendChild(hiddenField2);
             
        

        document.body.appendChild(form);
        form.submit();


        
    });



})
