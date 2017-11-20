// Validation for New Category Form
function validateForm() {
    var cName = document.forms["newcategoryForm"]["catName"].value;
    if (cName == "") {
        $('.new-category-alert').css("display", "block");
        return false;
    }
    
}

// Validation for Edit Item Form
function validateItemEditForm() {
	$('.new-item-alert-iName').css("display", "none");
	$('.new-item-alert-iDesc').css("display", "none");
	var cName = document.forms["editItemForm"]["catName"].value;
	var itemName = document.forms["editItemForm"]["itemName"].value;
	var itemDescription = document.forms["editItemForm"]["itemDescription"].value;
	if (itemName == "") {
		$('.new-item-alert-iName').css("display", "block");
		return false;
	}
	else if (itemDescription == "") {
		$('.new-item-alert-iDesc').css("display", "block");
		return false;
	}
}

// Validations for Edit Category form
function validateEditCategoryForm(){
	var cName = document.forms["editCategoryForm"]["catName"].value;
	if (cName == "") {
		$('.new-category-alert').css("display", "block");
		return false;
	}
}

// Click event function for box-grids to redirect to its 'redir' attribute value
$(document).ready(function(){
	$(".box_grid").click(function(){
		window.location.href = $(this).attr("redir");
	});
});



