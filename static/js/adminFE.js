$(document).ready(function(){
    $(".userManager").hide();
    $(".banManager").hide();
    $(".boardManager").show();

    $("#bAdminListItem").click(function (){
        $(".statistics").hide();
        $(".userManager").hide();
        $(".banManager").hide();
        $(".boardManager").show(250);
        $("#adminPanelHeader").text("Manage boards");
    });

    $("#uAdminListItem").click(function (){
        $(".statistics").hide();
        $(".userManager").show(250);
        $(".banManager").hide();
        $(".boardManager").hide();
        $("#adminPanelHeader").text("Manage users");
    });

    $("#mAdminListItem").click(function (){
        $(".statistics").hide();
        $(".userManager").hide();
        $(".banManager").show(250);
        $(".boardManager").hide();
        $("#adminPanelHeader").text("Manage bans");
    });

    $("#boardMgrCreateBoardForm").hide();
    $("#boardMgrCreateCategoryForm").hide();

    $("#boardMgrCreateNewBoard").click(function(){
        $("#boardMgrCreateCategoryForm").hide();
        $("#boardMgrCreateBoardForm").show(250);
    });

    $("#boardMgrCreateNewCategory").click(function(){
        $("#boardMgrCreateBoardForm").hide();
        $("#boardMgrCreateCategoryForm").show(250);
    });
});
