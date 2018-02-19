$(document).ready(function(){
    $("#delete_team_button").click(function(e){
        if (!confirm('팀을 삭제하시겠습니까?')){
            return false;
        }
    });
});

$(document).ready(function(){
    $("#delete_project_button").click(function(e){
        if (!confirm('프로젝트를 취소하겠습니까?')){
            return false;
        }
    });
});

$("#project_delete_form").submit(function(e){
    e.preventDefault();

    var url = '{% url "team:projectlist" %}'

    $.post(url)
        .done(function(r){
            $('project_list').remove(r);
        })
        .fail(function(r){
            alert('에러발생')
        })
})
