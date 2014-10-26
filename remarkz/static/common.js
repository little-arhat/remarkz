function _a(obj){
    return Array.prototype.slice.call(obj);
}

function all(sequence){
    for(var i=0; i < sequence.length; i++){
        if(!sequence[i])
            return false;
    }
    return true;
}

function clean_tag(tag){
    return encodeURIComponent(tag.trim());
}

function prepare_tags(str){
    return $.map(str.trim().split(' '), clean_tag).join('/');
}

function check_size(elmt){
    return function(_){
        return (len(elmt) < window.char_limit && len(elmt) > 0);
    }
}

function len(elmt){
    return elmt.val().trim().length;
}

function add_hint(elmt, func){
    elmt.addClass('hint')
    elmt.focus(function(){
        elmt.removeClass('hint');
        elmt.val('');
        elmt.focus(function(){});
    });
    if (func)
        func(elmt);
}

function handle_count(elmt, place){
    var left = window.char_limit - len(elmt);
    if(left < 0)
        place.addClass('error');
    else
        place.removeClass('error');
    place.html(left);
}


function button_guard(button){
    return function(){
        var conds = _a(arguments);
        if (all(conds))
            button.attr('disabled', '');
        else
            button.attr('disabled', 'disabled');
    }
}

function handle_submit(form_id, field_id, func){
    var frm = $('#' + form_id);
    return frm.submit(function(){
        var field = $('#' + field_id);
        var tags = prepare_tags(field.val());
        field.val('');
        var url = frm.attr('action');
        frm.attr('action', url + tags);
        if(func)
            return func(frm);
        else
            return true;
    });
}

function ctrl_enter(elmt, frm){
    elmt.keydown(function (e) {
        if ((e.ctrlKey || e.metaKey) && e.keyCode == 13) {
            frm.submit();
        }
    });
}
