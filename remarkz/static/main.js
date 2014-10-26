$(document).ready(function() {
    var texta = $('#item');
    var tags = $('#tags');
    var go = $('#go');
    var add = $('#add');
    var count = $('#count');

    handle_submit('post', 'tags', check_size(texta));
    handle_submit('search', 'tags');
    ctrl_enter(texta, $("#post"));

    go.attr('disabled', 'disabled');
    add.attr('disabled', 'disabled');

    var correct_tags = false;
    var correct_length = false;

    var add_guard = button_guard(add);
    var go_guard = button_guard(go);

    add_hint(tags, function(tags){
        tags.keyup(function(){
            correct_tags = tags.val().trim().length > 0

            go_guard(correct_tags);
            add_guard(correct_length, correct_tags);
        });
    });


    texta.keyup(function(){
        handle_count(texta, count);
        correct_length = check_size(texta)();

        add_guard(correct_length, correct_tags);
    });
    texta.keyup();

});
