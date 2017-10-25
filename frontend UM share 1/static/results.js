

$( document ).ready(function() {
    $('.sendThese').click(function(e){
        alert(e.currentTarget.innerText);

        var movieName = e.currentTarget.innerText;
        var user_email = $('#email').text();

        var form = document.createElement("form");
        form.setAttribute("method", 'post');
        form.setAttribute("action", '/get');

            
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
});