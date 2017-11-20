function Task(data) {
	this.name = data.name;
	this.description = data.description;
	this.order = data.order;
}

function TaskListViewModel() {
	var self = this;
	self.tasks = ko.observeArray([]);

	$.getJSON({% url 'getItems' cat_id %}, function(allData) {
        var mappedTasks = $.map(allData, function(item) { return new Task(item) });
        self.tasks(mappedTasks);
    });


}

ko.applyBindings(new TaskListViewModel());