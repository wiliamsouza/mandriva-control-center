import QtQuick 1.0
import "mandriva"


Rectangle {
    id: window
    width: 640
    height: 480

    Rectangle {
        id: header
        width: window.width
        height: 100
        opacity: 1
        clip: true
        color: "#483737"

        Image {
            id: mandrivaLogo
            source: "images/mandriva_logo.png"
            anchors.left: parent.left
            anchors.leftMargin: 12
            anchors.verticalCenter: parent.verticalCenter
        }

        Row {
            spacing: 15
            anchors.right:  parent.right
            anchors.rightMargin: 15
            anchors.verticalCenter: parent.verticalCenter
            children: [
                Image {
                    id: saveButton
                    source: "images/document-save.png"
                    opacity: 0.2
                },

                Image {
                    id: addUserButton
                    source: "images/list-add-user.png"
                    MouseArea {
                        anchors.fill: parent
                        onClicked: {
                            listView.model = userModel
                            listView.delegate = userDelegate
                            groupForm.visible = false
                            contentFlick.contentHeight = addUserForm.height
                            userForm.visible = false
                            addGroupForm.visible = false
                            addUserForm.visible = true
                            deleteGroup.visible = false
                            deleteUser.visible = true
                            deleteUser.opacity = 0.2
                        }
                    }
                },

                Image {
                    id: addGroupButton
                    source: "images/user-group-new.png"
                    MouseArea {
                        anchors.fill: parent
                        onClicked: {
                            listView.model = groupModel
                            listView.delegate = groupDelegate
                            groupForm.visible = false
                            contentFlick.contentHeight = addGroupForm.height
                            userForm.visible = false
                            addUserForm.visible = false
                            addGroupForm.visible = true
                            deleteUser.visible = false
                            deleteGroup.visible = true
                            deleteGroup.opacity = 0.2
                        }
                    }
                },

                Image {
                    id: deleteUser
                    source: "images/list-remove-user.png"
                    opacity: 0.2
                    MouseArea {
                        anchors.fill: parent
                        onClicked: {
                            if (deleteUser.opacity == 0.2)
                                console.log("button disabled")
                            else
                                scrollFormUser.message = "Do you really want to delete the user?"
                                scrollFormUser.state = "show"
                                //listView.currentIndex = 0
                        }
                    }
                },

                Image {
                    id: deleteGroup
                    source: "images/list-remove-user.png"
                    opacity: 0.2
                    visible: false
                    MouseArea {
                        anchors.fill: parent
                        onClicked: {
                            if (deleteGroup.opacity == 0.2)
                                console.log("button disabled")
                            else
                                scrollFormGroup.message = "Do you really want to delete the group?"
                                scrollFormGroup.state = "show"
                        }
                    }
                },

                Image {
                    id: refreshButton
                    source: "images/view-refresh.png"
                    MouseArea {
                        anchors.fill: parent
                        onClicked: {
                            controller.reflesh(groupModel)
                        }
                    }
                }
            ]
        }
    }

    Rectangle {
        id: sidebar
        y: header.height
        width: 240
        height: window.height - header.height
        clip: true
        color: "#916f6f"

        ListView {
            id: listView
            width: sidebar.width
            height: sidebar.height
            model: userModel
            delegate: userDelegate
            header: listViewHeader
            highlight: listViewHighlight
            highlightFollowsCurrentItem: true
        }
    }

    Rectangle {
        id: content
        x: sidebar.width
        y: header.height
        width: window.width - sidebar.width
        height: window.height - header.height
        clip: true
        color: "#6c5353"

        Rectangle {
            property alias message: messageGroup.text
            property bool status: false

            id: scrollFormGroup
            y: -height
            z: 10
            width: content.width - 100
            height: 80
            color: "#e3dbdb"
            anchors.horizontalCenter: parent.horizontalCenter

            Text {
                id: messageGroup
                text: ""
                color: "#241c1c"
                font.bold: true
                font.family: "Sans"
                anchors.horizontalCenter: parent.horizontalCenter
                anchors.top: parent.top
                anchors.topMargin: 10
            }


            Row {
                spacing: 10
                anchors.horizontalCenter:  parent.horizontalCenter
                anchors.bottom: parent.bottom

                MdvButton {
                    width: 40
                    text: "Ok"
                    MouseArea {
                        anchors.fill: parent
                        onClicked: {
                            scrollFormGroup.status = true
                            scrollFormGroup.state = ""
                            console.log("deleting group")
                            controller.deleteGroup(listView.currentIndex, listView.currentItem)
                            listView.currentIndex = 0
                        }
                    }
                }

                MdvButton {
                    text: "Cancel"
                    width: 80
                    MouseArea {
                        anchors.fill: parent
                        onClicked: {
                            scrollFormGroup.status = false
                            scrollFormGroup.state = ""
                        }
                    }
                }
            }

            states : State {
                name: "show"
                PropertyChanges { target: scrollFormGroup; y: 0}
            }

            transitions: Transition {
                NumberAnimation { properties: "y"; duration: 500 }
            }
        }

        Rectangle {
            property alias message: messageUser.text
            property bool status: false

            id: scrollFormUser
            y: -height
            z: 10
            width: content.width - 100
            height: 80
            color: "#e3dbdb"
            anchors.horizontalCenter: parent.horizontalCenter

            Text {
                id: messageUser
                text: ""
                color: "#241c1c"
                font.bold: true
                font.family: "Sans"
                anchors.horizontalCenter: parent.horizontalCenter
                anchors.top: parent.top
                anchors.topMargin: 10
            }


            Row {
                spacing: 10
                anchors.horizontalCenter:  parent.horizontalCenter
                anchors.bottom: parent.bottom

                MdvButton {
                    width: 40
                    text: "Ok"
                    MouseArea {
                        anchors.fill: parent
                        onClicked: {
                            scrollFormUser.status = true
                            scrollFormUser.state = ""
                            console.log("deleting user")
                            controller.deleteUser(listView.currentIndex, listView.currentItem)
                            listView.currentIndex = 0
                        }
                    }
                }

                MdvButton {
                    text: "Cancel"
                    width: 80
                    MouseArea {
                        anchors.fill: parent
                        onClicked: {
                            scrollFormUser.status = false
                            scrollFormUser.state = ""
                        }
                    }
                }
            }

            states : State {
                name: "show"
                PropertyChanges { target: scrollFormUser; y: 0}
            }

            transitions: Transition {
                NumberAnimation { properties: "y"; duration: 500 }
            }
        }

        Flickable {
            id: contentFlick
            anchors.fill: parent
            contentWidth: content.width
            contentHeight: userForm.height

            Grid {
                id: userForm
                visible: false
                columns: 2
                spacing: 8
                anchors.left: parent.left
                anchors.leftMargin: 12
                anchors.top: parent.top
                anchors.topMargin: 12


                // User data **************************************************
                Text {
                    text: "User data"
                    color: "#241c1c"
                    font.bold: true
                    font.pixelSize: 20
                    font.family: "Sans"
                }
                Text {
                    text: " "
                }

                Text {
                    text: "Full name:"
                    color: "#e3dbdb"
                    font.bold: true
                    font.pixelSize: 15
                    font.family: "Sans"
                }
                MdvTextInput {
                    id: fullName
                    width: 215
                }

                Text {
                    text: "Username:"
                    color: "#e3dbdb"
                    font.bold: true
                    font.pixelSize: 15
                    font.family: "Sans"
                }
                MdvTextInput {
                    id: userName
                    width: 215
                }

                Text {
                    text: "Password:"
                    color: "#e3dbdb"
                    font.bold: true
                    font.pixelSize: 15
                    font.family: "Sans"
                }
                MdvTextInput {
                    id: password
                    width: 215
                    text: "password"
                    echoMode: TextInput.Password
                }

                Text {
                    text: "Confirm password:"
                    color: "#e3dbdb"
                    font.bold: true
                    font.pixelSize: 15
                    font.family: "Sans"
                }
                MdvTextInput {
                    id: confirmPassword
                    width: 215
                    text: "password"
                    echoMode: TextInput.Password
                }

                Text {
                    text: "Login shell:"
                    color: "#e3dbdb"
                    font.bold: true
                    font.pixelSize: 15
                    font.family: "Sans"
                }
                MdvTextInput {
                    id: loginShell
                    width: 215
                }

                Text {
                    text: "Home Directory:"
                    color: "#e3dbdb"
                    font.bold: true
                    font.pixelSize: 15
                    font.family: "Sans"
                }
                MdvTextInput {
                    id: homeDirectory
                    width: 215
                }


                // Account info ***********************************************
                Text {
                    text: "Account info"
                    color: "#241c1c"
                    font.bold: true
                    font.pixelSize: 20
                    font.family: "Sans"
                }
                Text {
                    text: " "
                }

                Text {
                    text: "Account expires:"
                    color: "#e3dbdb"
                    font.bold: true
                    font.pixelSize: 15
                    font.family: "Sans"
                }
                MdvCheckBox {
                    objectName: 'shadowExpire'
                    id: shadowExpire
                }


                Text {
                    text: "Expiration Date:"
                    color: "#e3dbdb"
                    font.bold: true
                    font.pixelSize: 15
                    font.family: "Sans"
                }
                MdvTextInput {
                    id: expirationDate
                    width: 215
                }

                Text {
                    text: "Lock account:"
                    color: "#e3dbdb"
                    font.bold: true
                    font.pixelSize: 15
                    font.family: "Sans"
                }
                MdvCheckBox {
                    objectName: 'lockAccount'
                    id: lockAccount
                }


                Text {
                    text: "Icon:"
                    color: "#e3dbdb"
                    font.bold: true
                    font.pixelSize: 15
                    font.family: "Sans"
                }
                Text {
                    text: " "
                }


                // Password info **********************************************
                Text {
                    text: "Password info"
                    color: "#241c1c"
                    font.bold: true
                    font.pixelSize: 20
                    font.family: "Sans"
                }
                Text {
                    text: " "
                }

                Text {
                    text: "Change allowed:" //"Days before change allowed:"
                    color: "#e3dbdb"
                    font.bold: true
                    font.pixelSize: 15
                    font.family: "Sans"
                }
                MdvTextInput {
                    id: shadowMin
                    width: 215
                }

                Text {
                    text: "Change required:" //"Days before change required:"
                    color: "#e3dbdb"
                    font.bold: true
                    font.pixelSize: 15
                    font.family: "Sans"
                }
                MdvTextInput {
                    id: shadowMax
                    width: 215
                }

                Text {
                    text: "Warning change:" //"Days warning before change:"
                    color: "#e3dbdb"
                    font.bold: true
                    font.pixelSize: 15
                    font.family: "Sans"
                }
                MdvTextInput {
                    id: shadowWarning
                    width: 215
                }

                Text {
                    text: "Account inactive:" //"Days before account inactive:"
                    color: "#e3dbdb"
                    font.bold: true
                    font.pixelSize: 15
                    font.family: "Sans"
                }
                MdvTextInput {
                    id: shadowInactive
                    width: 215
                }

                Text {
                    text: "Last changed:" //"User last changed password on:"
                    color: "#e3dbdb"
                    font.bold: true
                    font.pixelSize: 15
                    font.family: "Sans"
                }
                Text {
                    id: shadowLastChange
                    text: "Sun Dec 26 2010"
                }

                // Groups *****************************************************
                Text {
                    text: " "
                }
                Text {
                    text: "Groups"
                    color: "#241c1c"
                    font.bold: true
                    font.pixelSize: 20
                    font.family: "Sans"
                }

                Text {
                    text: " "
                }
                ListView {
                    id: groupSelectListView
                    width: 215
                    height: 300
                    model: allGroupModel
                    delegate: groupSelectDelegate
                    clip: true
                    //header: listViewHeader
                    //highlightFollowsCurrentItem: true
                    //focus: true
                }
            }


            Grid {
                id: groupForm
                visible: false
                columns: 2
                spacing: 8
                anchors.left: parent.left
                anchors.leftMargin: 12
                anchors.top: parent.top
                anchors.topMargin: 12

                // Line #1
                Text {
                    text: "Group name:"
                    color: "black"
                    opacity: 0.6
                    font.bold: true
                    font.pixelSize: 15
                }
                MdvTextInput {
                    id: groupName
                    property string oldGroupName: ""
                    objectName: "groupName"
                    width: 215
                }

                // Groups *****************************************************
                Text {
                    text: " "
                }
                Text {
                    text: "Group users"
                    color: "#241c1c"
                    font.bold: true
                    font.pixelSize: 20
                    font.family: "Sans"
                }

                Text {
                    text: " "
                }

                ListView {
                    id: userSelectListView
                    width: 215
                    height: 300
                    model: allUserModel
                    delegate: userSelectDelegate
                    clip: true
                    visible: true
                    //header: listViewHeader
                    //highlightFollowsCurrentItem: true
                    //focus: true
                }
                Text {
                    text: " "
                }
                MdvButton {
                    width: 100
                    text: "Save"
                    MouseArea {
                        anchors.fill: parent
                        onClicked: {
                            controller.ModifyGroup(groupForm)
                        }
                    }
                }
            }

            Grid {
                id: addUserForm
                visible: false
                columns: 2
                spacing: 8
                anchors.left: parent.left
                anchors.leftMargin: 12
                anchors.top: parent.top
                anchors.topMargin: 12


                Text {
                    text: "New user"
                    color: "#241c1c"
                    font.bold: true
                    font.pixelSize: 20
                    font.family: "Sans"
                }
                Text {
                    text: " "
                }

                Text {
                    text: "Full name:"
                    color: "#e3dbdb"
                    font.bold: true
                    font.pixelSize: 15
                    font.family: "Sans"
                }
                MdvTextInput {
                    objectName: 'addFullName'
                    //id: addFullName
                    width: 215
                }

                Text {
                    text: "Username:"
                    color: "#e3dbdb"
                    font.bold: true
                    font.pixelSize: 15
                    font.family: "Sans"
                }
                MdvTextInput {
                    objectName: 'addUserName'
                    width: 215
                    onTextChanged: addHomeDirectory.text = "/home/" + text
                }

                Text {
                    text: "Password:"
                    color: "#e3dbdb"
                    font.bold: true
                    font.pixelSize: 15
                    font.family: "Sans"
                }
                MdvTextInput {
                    objectName: 'addPassword'
                    width: 215
                    echoMode: TextInput.Password
                }

                Text {
                    text: "Confirm password:"
                    color: "#e3dbdb"
                    font.bold: true
                    font.pixelSize: 15
                    font.family: "Sans"
                }
                MdvTextInput {
                    objectName: 'addConfirmPassword'
                    width: 215
                    echoMode: TextInput.Password
                }

                Text {
                    text: "Login shell:"
                    color: "#e3dbdb"
                    font.bold: true
                    font.pixelSize: 15
                    font.family: "Sans"
                }
                MdvTextInput {
                    objectName: 'addLoginShell'
                    width: 215
                    text: "/bin/bash"
                    //model: shellModel
                    //currentIndex: 1
                }

                Text {
                    text: "Create home:"
                    color: "#e3dbdb"
                    font.bold: true
                    font.pixelSize: 15
                    font.family: "Sans"
                }
                MdvCheckBox {
                    objectName: 'addCreateHomeDirectory'
                    checked: true
                }

                Text {
                    text: "Home Directory:"
                    color: "#e3dbdb"
                    font.bold: true
                    font.pixelSize: 15
                    font.family: "Sans"
                }
                MdvTextInput {
                    objectName: 'addHomeDirectory'
                    id: addHomeDirectory
                    width: 215
                    text: "/home/"
                }

                Text {
                    text: "Private group:"
                    color: "#e3dbdb"
                    font.bold: true
                    font.pixelSize: 15
                    font.family: "Sans"
                }
                MdvCheckBox {
                    objectName: 'addCreatePrivateGroup'
                    checked: true
                }

                Text {
                    text: "Specify user ID:"
                    color: "#e3dbdb"
                    font.bold: true
                    font.pixelSize: 15
                    font.family: "Sans"
                }
                MdvCheckBox {
                    objectName: 'addSpecifyUserId'
                    onPressedChanged: !checked ? addUserId.opacity = 0.2: addUserId.opacity = 1
                }

                Text {
                    text: "User ID:"
                    color: "#e3dbdb"
                    font.bold: true
                    font.pixelSize: 15
                    font.family: "Sans"
                }
                MdvTextInput {
                    objectName: 'addUserId'
                    id: addUserId
                    width: 215
                    opacity: 0.2
                    //text: unusedUid
                }

                Text {
                    text: " "
                }
                MdvButton {
                    width: 100
                    text: "Save"
                    MouseArea {
                        anchors.fill: parent
                        onClicked: {
                            controller.addUser(addUserForm)
                        }
                    }
                }
            }

            Grid {
                id: addGroupForm
                visible: false
                columns: 2
                spacing: 8
                anchors.left: parent.left
                anchors.leftMargin: 12
                anchors.top: parent.top
                anchors.topMargin: 12


                Text {
                    text: "New group"
                    color: "#241c1c"
                    font.bold: true
                    font.pixelSize: 20
                    font.family: "Sans"
                }
                Text {
                    text: " "
                }

                Text {
                    text: "Group name:"
                    color: "#e3dbdb"
                    font.bold: true
                    font.pixelSize: 15
                    font.family: "Sans"
                }
                MdvTextInput {
                    objectName: 'addGroupName'
                    width: 215
                }

                Text {
                    text: "Specify group ID:"
                    color: "#e3dbdb"
                    font.bold: true
                    font.pixelSize: 15
                    font.family: "Sans"
                }
                MdvCheckBox {
                    objectName: 'addSpecifyGroupId'
                    onPressedChanged: !checked ? addGroupId.opacity = 0.2: addGroupId.opacity = 1
                }

                Text {
                    text: "Group ID:"
                    color: "#e3dbdb"
                    font.bold: true
                    font.pixelSize: 15
                    font.family: "Sans"
                }
                MdvTextInput {
                    objectName: "addGroupId"
                    id: addGroupId
                    width: 215
                    opacity: 0.2
                    //text: unusedGid
                }

                Text {
                    text: " "
                }
                MdvButton {
                    width: 100
                    text: "Save"
                    MouseArea {
                        anchors.fill: parent
                        onClicked: {
                            controller.addGroup(addGroupForm)
                        }
                    }
                }
            }
        }
    }

    Component {
        id: listViewHeader
        Column {
            id: col
            Row {
                spacing: 10
                anchors.horizontalCenter:  parent.horizontalCenter
                MdvButton {
                    width: (listView.width / 2) - 5
                    text: "Users"
                    MouseArea {
                        anchors.fill: parent
                        onClicked: {
                            listView.model = userModel
                            listView.delegate = userDelegate
                            groupForm.visible = false
                            contentFlick.contentHeight = userForm.height
                            //userForm.visible = true
                            addUserForm.visible = false
                            addGroupForm.visible = false
                            deleteUser.opacity = 0.2
                            deleteGroup.visible = false
                            deleteUser.visible = true
                        }
                    }
                }
                MdvButton {
                    text: "Groups"
                    width: (listView.width / 2) - 5
                    MouseArea {
                        anchors.fill: parent
                        onClicked: {
                            listView.model = groupModel
                            listView.delegate = groupDelegate
                            userForm.visible = false
                            contentFlick.contentHeight = groupForm.height
                            //groupForm.visible = true
                            addUserForm.visible = false
                            addGroupForm.visible = false
                            deleteGroup.opacity = 0.2
                            deleteUser.visible = false
                            deleteGroup.visible = true
                        }
                    }
                }
            }
            MdvTextInput {
                id: searchBox
                width: listView.width
                height: 22
                hint: "Search"
            }
        }
    }

    Component {
        id: userDelegate
        Rectangle {
            height: 60
            width: listView.width

            color: ((index % 2 == 0) ? "#c8b7b7" : "#ac9393")
            Row {
                anchors.verticalCenter: parent.verticalCenter
                spacing: 12
                anchors.left: parent.left
                anchors.leftMargin: 10
                children: [
                    Text {
                        anchors.verticalCenter: parent.verticalCenter
                        text: model.user.uid
                        color: "#d45500"
                        font.bold: true
                        font.pixelSize: 16
                        font.family: "Sans"
                    },
                    Column {
                        anchors.verticalCenter: parent.verticalCenter
                        spacing: 3
                        children: [
                            Text {
                                objectName: "delegateUserName"
                                text: model.user.username
                                color: "#483737"
                                font.bold: true
                                font.pixelSize: 16
                                font.family: "Sans"
                            },
                            Text {
                                text: model.user.fullname
                                color: "#6c5353"
                                font.pixelSize: 12
                                font.family: "Sans"
                            }
                        ]
                    }
                ]
            }
            MouseArea {
                anchors.fill: parent
                onClicked: {
                    listView.currentIndex = index
                    fullName.text = model.user.fullname
                    userName.text = model.user.username
                    loginShell.text = model.user.login_shell
                    homeDirectory.text = model.user.home_directory
                    shadowExpire.checked = model.user.shadow_expire
                    expirationDate.text = model.user.expiration_date
                    lockAccount.checked = model.user.islocked
                    shadowMin.text = model.user.shadow_min
                    shadowMax.text = model.user.shadow_max
                    shadowWarning.text = model.user.shadow_warning
                    shadowInactive.text = model.user.shadow_inactive
                    shadowLastChange.text = model.user.shadow_last_change
                    deleteUser.opacity = 1
                    controller.selectGroupByUser(model.user.username)
                    // keep this lines at end
                    groupForm.visible = false
                    addGroupForm.visible = false
                    addUserForm.visible = false
                    userForm.visible = true
                    contentFlick.contentHeight = userForm.height
                }
            }
        }
    }

    Component {
        id: userSelectDelegate
        Rectangle {
            height: 30
            width: userSelectListView.width
            color: ((index % 2 == 0) ? "#c8b7b7" : "#ac9393")
            Row {
                anchors.verticalCenter: parent.verticalCenter
                spacing: 12
                anchors.left: parent.left
                anchors.leftMargin: 10
                children: [
                    Text {
                        id: checkbox
                        text: "✔"
                        font.pixelSize: 18
                        font.bold: true
                        opacity: ((model.user.ischecked) ? 1.0 : 0.1)
                        color: "white"
                        //anchors {
                        //    verticalCenter: parent.verticalCenter
                        //    right: parent.right
                        //    rightMargin: 5
                       // }
                    },
                    Text {
                        text: model.user.username
                        color: "#483737"
                        font.bold: true
                        font.pixelSize: 16
                        font.family: "Sans"
                        MouseArea {
                            anchors.fill: parent
                            onClicked: {
                                controller.toggledUser(allUserModel, model.user)
                            }
                        }
                    }
                ]
            }
        }
    }

    Component {
        id: groupDelegate
        Rectangle {
            height: 60
            width: listView.width
            color: ((index % 2 == 0) ? "#c8b7b7" : "#ac9393")
            Row {
                anchors.verticalCenter: parent.verticalCenter
                spacing: 12
                anchors.left: parent.left
                anchors.leftMargin: 10
                children: [
                    Text {
                        anchors.verticalCenter: parent.verticalCenter
                        text: model.group.gid
                        color: "#d45500"
                        font.bold: true
                        font.pixelSize: 16
                        font.family: "Sans"
                    },
                    Column {
                        anchors.verticalCenter: parent.verticalCenter
                        children: [
                            Text {
                                objectName: "delegateGroupName"
                                text: model.group.groupname
                                color: "#483737"
                                font.bold: true
                                font.pixelSize: 16
                                font.family: "Sans"
                            }
                        ]
                    }
                ]
            }
            MouseArea {
                anchors.fill: parent
                onClicked: {
                    listView.currentIndex = index
                    groupName.text = model.group.groupname
                    groupName.oldGroupName = model.group.groupname
                    deleteGroup.opacity = 1
                    controller.selectUserByGroup(model.group.groupname)
                    // keep this lines at end
                    userForm.visible = false
                    addUserForm.visible = false
                    addGroupForm.visible = false
                    contentFlick.contentHeight = groupForm.height
                    groupForm.visible = true
                }
            }
        }
    }

    Component {
        id: groupSelectDelegate
        Rectangle {
            height: 30
            width: groupSelectListView.width
            color: ((index % 2 == 0) ? "#c8b7b7" : "#ac9393")
            Row {
                anchors.verticalCenter: parent.verticalCenter
                spacing: 12
                anchors.left: parent.left
                anchors.leftMargin: 10
                children: [
                    Text {
                        id: checkbox
                        text: "✔"
                        font.pixelSize: 18
                        font.bold: true
                        opacity: ((model.group.ischecked) ? 1.0 : 0.1)
                        color: "white"
                        //anchors {
                        //    verticalCenter: parent.verticalCenter
                        //    right: parent.right
                        //    rightMargin: 5
                       // }
                    },
                    Text {
                        text: model.group.groupname
                        color: "#483737"
                        font.bold: true
                        font.pixelSize: 16
                        font.family: "Sans"
                        MouseArea {
                            anchors.fill: parent
                            onClicked: {
                                controller.toggledGroup(allGroupModel, model.group)
                            }
                        }
                    }
                ]
            }
        }
    }

    Component {
        id: listViewHighlight
        Rectangle {
            color: "lightsteelblue"
            radius: 8
            y: listView.currentItem.y
            z: 2
            opacity: 0.4
            Behavior on y {
                SpringAnimation {
                    spring: 3
                    damping: 0.2
                }
            }
        }
    }
}
