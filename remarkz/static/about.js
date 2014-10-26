$(document).ready(function() {
    var correct_tags = false;

    handle_submit('bookmarklet', 'tags');
    add_hint($("#tags"), function(tags){
        tags.keyup(function(){
            correct_tags = len(tags) > 0

            go_guard(correct_tags);
        });
    });

    var tags = $('#tags');
    var go = $('#go');
    var go_guard = button_guard(go);
    go.attr('disabled', 'disabled');

    handle_submit('bookmarklet', 'tags', function(){correct_tags});



});

