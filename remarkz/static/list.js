$(document).ready(function() {
    var texta = $("#item");
    var add_guard = button_guard($("#add"));
    var correct_length = false;
    var count = $("#count");

    ctrl_enter(texta, $("#post"));

    texta.keyup(function(){
        handle_count(texta, count);
        correct_length = check_size(texta)();

        add_guard(correct_length);
    });
    texta.keyup();

    $("#post").submit(function(){
        return correct_length;
    });

});
