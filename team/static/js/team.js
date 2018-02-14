$(document).ready(function(){
    $("#delete_team_button").click(function(e){
        if (!confirm('팀을 삭제하시겠습니까?')){
            return false;
        }
    });
});
