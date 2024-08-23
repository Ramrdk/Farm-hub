function check_id()
{
    textbox=document.getElementById("track_order_textbox").value;
    button=document.getElementById("track_order_button");

    if(textbox=='')
        {
            alert('Please enter Order ID for tracking');
        }
    else{
        button.type="submit";
        button.submit();
    }
}