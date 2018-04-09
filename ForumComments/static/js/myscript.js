var app = angular.module('MyApp',['ngMaterial','ngMessages']);

app.component('comment', {
    bindings: {
        socket: '<',
        userId: '<',
        userFirstName: '<',
        userLastName: '<',
        courseId: '<',
        roomName: '<',
        comment: '='
    },
    template:   `<div layout="column" ng-style="{'padding': '0px'}">
                    <div layout-padding md-whiteframe="3" layout="column" ng-style="{'background': 'linear-gradient(to right, #F48FB1, #FCE4EC)' }">
                        <label class="md-title">{{$ctrl.comment.user_first_name}} {{$ctrl.comment.user_last_name}}</label>
                        <label class="md-body-1">{{$ctrl.comment.comment}}</label>
                    </div>
                    <div layour="row" flex layout="end end">
                        <md-input-container flex>
                            <label>Reply</label>
                            <input type="text" ng-model="$ctrl.new_comment" flex>
                        </md-input-container>
                        <md-button ng-click="$ctrl.onSend($ctrl.comment.id, 0)" class="md-raised md-primary" ng-style="{'height': '36px'}" ng-disabled="!$ctrl.new_comment">Send</md-button>
                        <md-button ng-click="$ctrl.onSend($ctrl.comment.id, 1)" class="md-raised md-warn" ng-style="{'height': '36px'}">Delete</md-button>
                    </div>
                    <comment-list ng-if="$ctrl.comment.children.length > 0" collection="$ctrl.comment.children" socket="$ctrl.socket" user-id="$ctrl.userId" user-first-name="$ctrl.userFirstName" user-last-name="$ctrl.userLastName" course-id="$ctrl.courseId" room-name="$ctrl.roomName"></comment-list>
                </div>`,
    controller: function(){
        var self = this;

        self.onSend = function(parent_id, event_type){
            console.log('Sending...')
            self.socket.send(
                JSON.stringify(
                    {
                        event_type: event_type,
                        data: {
                            user_id         : self.userId,
                            user_first_name : self.userFirstName,
                            user_last_name  : self.userLastName,
                            course_id       : self.roomName,
                            comment         : self.new_comment,
                            parent_id       : parent_id,
                        } 
                    }
                )
            )
        }
    }
});


app.component('commentList', {
    bindings: {
        socket: '<',
        userId: '<',
        userFirstName: '<',
        userLastName: '<',
        courseId: '<',
        roomName: '<',
        collection: '='
    },
    template:   `<div layout-padding layout="column">
                    <comment ng-repeat="comment_obj in $ctrl.collection" comment="comment_obj" socket="$ctrl.socket" user-id="$ctrl.userId" user-first-name="$ctrl.userFirstName" user-last-name="$ctrl.userLastName" course-id="$ctrl.courseId" room-name="$ctrl.roomName"></comment> 
                </div>`,
});

var ctrl = {};

app.controller('MainController', function($scope){
    var self = this;
    ctrl = self;
    self.connection_status = 'Disconnected';
    self.user_id = 1;
    self.user_first_name = 'Priyanshu';
    self.user_last_name = 'Bhatnagar';
    self.courseId = 1;
    self.room_name = 1;

    self.connect = function(){
        console.log('Connecting... ')
        self.socket = new WebSocket('ws://' + window.location.host + '/ws/forum/' + self.room_name + '/');

        self.socket.onmessage = self.onReceive;
        self.socket.onclose = self.onDisconnect;

        console.log('Connected!')
        self.connection_status = 'Connected';
        //$scope.$apply();
    }

    self.onDisconnect = function(e){
        console.error('Chat socket closed unexpectedly');
        self.connection_status = 'Disconnected';
    }

    self.disconnect = function(){
        self.socket.close();
        self.connection_status = 'Disconnected';
    }

    self.onReceive = function(e){
        var data = JSON.parse(e.data);
        console.log('Received: ')
        console.log(data);
        self.comment_list = data;
        $scope.$apply();
    }
});