//import Qt 4.7
import QtQuick 1.0
import Qt.labs.Mx 1.0

Item {
    id: window
    width: 640
    height: 480

    Item {
        id: header
        width: window.width
        height: 100
        opacity: 1
        clip: true

        Row {
            spacing: 12
            Image {
                id: addButton
                source: "images/list-add-user.png"
            }
            Image {
                id: editButton
                source: "images/user-properties.png"
            }
            Image {
                id: deleteButton
                source: "images/list-remove-user.png"
            }
            Image {
                id: refreshButton
                source: "images/view-refresh.png"
            }
        }
    }

    Item {
        id: left
        y: header.height
        width: 240
        height: window.height - header.height
        clip: true

        ListView {
            id: listView
            width: left.width
            height: left.height
            model: userModel
            delegate: userDelegate
            highlight: listViewHighlight
            highlightFollowsCurrentItem: true
            header: listViewHeader
            focus: true
            // TODO: How to manage user keyboard events inside a ListView
            //       that use highlight.
            //Keys.onDownPressed: {
            //    console.log('Key Down was pressed');
            //    event.accepted = true;
            //}
            //Keys.onUpPressed: {
            //    console.log('Key Up was pressed');
            //    event.accepted = true;
            //}
        }
    }

    Rectangle {
        id: right
        x: left.width
        y: header.height
        width: window.width - left.width
        height: window.height - header.height
        clip: true
        color: "lightblue"

        Flickable {
            id: rightFlick
            anchors.fill: parent
            contentWidth: right.width
            contentHeight: userForm.height

        Grid {
            id: userForm
            visible: false
            columns: 2
            spacing: 12
            anchors.left: parent.left
            anchors.leftMargin: 12
            anchors.top: parent.top
            anchors.topMargin: 12


            // User data
            Text {
                text: "User data"
                color: "red"
                opacity: 0.6
                font.bold: true
                font.pixelSize: 20
            }
            Text {
                text: " "
            }

            Text {
                text: "Full name:"
                color: "black"
                opacity: 0.6
                font.bold: true
                font.pixelSize: 15
            }
            TextInput {
                id: fullName
                width: 215
                text: "full name"
                selectByMouse: true
            }

            Text {
                text: "Username:"
                color: "black"
                opacity: 0.6
                font.bold: true
                font.pixelSize: 15
            }
            TextInput {
                id: userName
                width: 215
                text: "username"
                selectByMouse: true
            }

            Text {
                text: "Password:"
                color: "black"
                opacity: 0.6
                font.bold: true
                font.pixelSize: 15
            }
            TextInput {
                id: password
                width: 215
                text: "password"
                selectByMouse: true
                echoMode: TextInput.Password
            }

            Text {
                text: "Confirm password:"
                color: "black"
                opacity: 0.6
                font.bold: true
                font.pixelSize: 15
            }
            TextInput {
                id: confirmPassword
                width: 215
                text: "password"
                selectByMouse: true
                echoMode: TextInput.Password
            }

            Text {
                text: "Login shell:"
                color: "black"
                opacity: 0.6
                font.bold: true
                font.pixelSize: 15
            }
            TextInput {
                id: loginShell
                width: 215
                text: "login shell"
                selectByMouse: true
            }

            Text {
                text: "Home Directory:"
                color: "black"
                opacity: 0.6
                font.bold: true
                font.pixelSize: 15
            }
            TextInput {
                id: homeDirectory
                width: 215
                text: "home"
                selectByMouse: true
            }


            // Account info
            Text {
                text: "Account info"
                color: "red"
                opacity: 0.6
                font.bold: true
                font.pixelSize: 20
            }
            Text {
                text: " "
            }

            Text {
                text: "Account expires:"
                color: "black"
                opacity: 0.6
                font.bold: true
                font.pixelSize: 15
            }
            TextInput {
                id: accountExpires
                width: 215
                //text: ""
                selectByMouse: true
                inputMask: "0000-00-00"
            }

            Text {
                text: "Lock account:"
                color: "black"
                opacity: 0.6
                font.bold: true
                font.pixelSize: 15
            }
            TextInput {
                id: lockAccount
                width: 215
                text: "no"
                selectByMouse: true
            }

            Text {
                text: "Icon:"
                color: "black"
                opacity: 0.6
                font.bold: true
                font.pixelSize: 15
            }
            Text {
                text: " "
            }


            // Password info
            Text {
                text: "Password info"
                color: "red"
                opacity: 0.6
                font.bold: true
                font.pixelSize: 20
            }
            Text {
                text: " "
            }

            Text {
                text: "Password Expiration:"
                color: "black"
                opacity: 0.6
                font.bold: true
                font.pixelSize: 15
            }
            TextInput {
                id: passwordExpiration
                width: 215
                text: "no"
                selectByMouse: true
            }

            Text {
                text: "Days before change allowed:"
                color: "black"
                opacity: 0.6
                font.bold: true
                font.pixelSize: 15
            }
            TextInput {
                id: changedAllowed
                width: 215
                text: "changed allowed"
                selectByMouse: true
            }

            Text {
                text: "Days before change required:"
                color: "black"
                opacity: 0.6
                font.bold: true
                font.pixelSize: 15
            }
            TextInput {
                id: changedRequired
                width: 215
                text: "changed required"
                selectByMouse: true
            }

            Text {
                text: "Days warning before change:"
                color: "black"
                opacity: 0.6
                font.bold: true
                font.pixelSize: 15
            }
            TextInput {
                id: warningChange
                width: 215
                text: "warning change"
                selectByMouse: true
            }

            Text {
                text: "Days before account inactive:"
                color: "black"
                opacity: 0.6
                font.bold: true
                font.pixelSize: 15
            }
            TextInput {
                id: accountInactive
                width: 215
                text: "account inactive"
                selectByMouse: true
            }

            Text {
                text: "User last changed password on:"
                color: "black"
                opacity: 0.6
                font.bold: true
                font.pixelSize: 15
            }
            Text {
                text: "Sun Dec 26 2010"
            }

            // Groups
            Text {
                text: "Groups"
                color: "red"
                opacity: 0.6
                font.bold: true
                font.pixelSize: 20
            }
            Text {
                text: " "
            }
        }

        Grid {
            id: groupForm
            visible: false
            columns: 2
            spacing: 12
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
            TextInput {
                id: groupName
                width: 215
                text: "group name"
                focus: true
                selectByMouse: true
            }
        }
        }

        // Not used variable scope problem
        //Loader {
        //    id: rightLoader
        //    anchors.fill: parent
        //    sourceComponent: UserForm{} //Welcome {}
        //}
    }

    Component {
        id: listViewHighlight
        Rectangle {
            color: "lightsteelblue"
            radius: 8
            y: listView.currentItem.y
            Behavior on y {
                SpringAnimation {
                    spring: 3
                    damping: 0.2
                }
            }
        }
    }

    Component {
        id: listViewHeader
        ButtonGroup {
            width: col.width
            height: col.height
            Column {
                id: col
                Row {
                    Button {
                        text: "Users"
                        checkable: true
                        checked: true
                        onClicked: {
                            listView.model = userModel
                            listView.delegate = userDelegate
                            groupForm.visible = false
                            rightFlick.contentHeight = userForm.height
                            userForm.visible = true
                            addButton.source = "images/list-add-user.png"
                            editButton.source ="images/user-properties.png"
                            deleteButton.source = "images/list-remove-user.png"
                        }
                    }
                    Button {
                        text: "Groups"
                        checkable: true
                        onClicked: {
                            listView.model = groupsModel
                            listView.delegate = groupDelegate
                            userForm.visible = false
                            rightFlick.contentHeight = groupForm.height
                            groupForm.visible = true
                            addButton.source = "images/user-group-new.png"
                            editButton.source ="images/user-group-properties.png"
                            deleteButton.source = "images/user-group-delete.png"
                        }
                    }
                }
                Entry {
                    id: searchBox
                    width: listView.width
                    height: 28
                    hint: "Search"
                    leftIconSource: "images/system-search.png";
                    onLeftIconClicked: searchBox.hint = "Searching...";
                    rightIconSource: "images/edit-delete.png";
                    onRightIconClicked: searchBox.hint = "Search";
                }
            }
        }
    }

    ListModel {
        id: usersModel
        ListElement {
            username: "wiliam"
            fullname: "Wiliam Souza"
            uid: "500"
        }
        ListElement {
            username: "paula"
            fullname: "Ana Paula"
            uid: "501"
        }
        ListElement {
            username: "caio"
            fullname: "Caio Eduardo"
            uid: "502"
        }
        ListElement {
            username: "Julia"
            fullname: "Ana Julia"
            uid: "503"
        }
        ListElement {
            username: "john"
            fullname: "John Doe"
            uid: "666"
        }
    }

    Component {
        id: userDelegate
        Item {
            height: 45
            width: listView.width
            Column {
                anchors.verticalCenter: parent.verticalCenter
                children: [
                    Text {
                        //id: userName
                        text: model.user.username
                        color: "black"
                        opacity: 0.6
                        font.bold: true
                    },
                    Text {
                        //id: fullName
                        text: model.user.fullname
                        color: "grey"
                    }
                ]
            }
            MouseArea {
                anchors.fill: parent
                onClicked: {
                    console.log("Clicked")
                    listView.currentIndex = index
                    fullName.text = model.user.fullname
                    userName.text = model.user.username
                    loginShell.text = model.user.login_shell
                    homeDirectory.text = model.user.home_directory

                    // keep this two line at end
                    groupForm.visible = false
                    userForm.visible = true
                }
            }
        }
    }

    ListModel {
        id: groupsModel
        ListElement {
            groupname: "wiliam"
            members: "wiliam"
        }

        ListElement {
            groupname: "paula"
            members: "paula"
        }

        ListElement {
            groupname: "caio"
            members: "caio"
        }

        ListElement {
            groupname: "Julia"
            members: "julia"
        }
    }

    Component {
        id: groupDelegate
        Item {
            height: 45
            width: listView.width
            Column {
                anchors.verticalCenter: parent.verticalCenter
                children: [
                    Text {
                        //id: groupName
                        text: groupname
                        color: "black"
                        opacity: 0.6
                        font.bold: true
                    }
                ]
            }
            MouseArea {
                anchors.fill: parent
                onClicked: {
                    console.log("Clicked")
                    listView.currentIndex = index
                    groupName.text = groupname

                    // keep this two line at end
                    userForm.visible = false
                    groupForm.visible = true
                }
            }
        }
    }
}
