import QtQuick 1.0
//import Qt.labs.Mx 1.0
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
                },
                Image {
                    id: addGroupButton
                    source: "images/user-group-new.png"
                },
                Image {
                    id: deleteButton
                    source: "images/list-remove-user.png"
                    opacity: 0.2
                    MouseArea {
                        anchors.fill: parent
                        //controller.Delete
                    }
                },
                Image {
                    id: refreshButton
                    source: "images/view-refresh.png"
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
            model: usersModel
            delegate: userDelegate
            header: listViewHeader
            highlightFollowsCurrentItem: true
            focus: true
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

        Flickable {
            id: contentFlick
            anchors.fill: parent
            contentWidth: content.width
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
                    //text: "full name"
                    //selectByMouse: true
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
                    //text: "username"
                    //selectByMouse: true
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
                    //selectByMouse: true
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
                    //selectByMouse: true
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
                    //text: "login shell"
                    //selectByMouse: true
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
                    //text: "home"
                    //selectByMouse: true
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
                MdvTextInput {
                    id: accountExpires
                    width: 215
                    //text: ""
                    //selectByMouse: true
                    //inputMask: "0000-00-00"
                }

                Text {
                    text: "Lock account:"
                    color: "#e3dbdb"
                    font.bold: true
                    font.pixelSize: 15
                    font.family: "Sans"
                }
                MdvTextInput {
                    id: lockAccount
                    width: 215
                    //text: "no"
                    //selectByMouse: true
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
                    text: "Expiration:" //"Password expiration:"
                    color: "#e3dbdb"
                    font.bold: true
                    font.pixelSize: 15
                    font.family: "Sans"
                }
                MdvTextInput {
                    id: passwordExpiration
                    width: 215
                    //text: "no"
                    //selectByMouse: true
                }

                Text {
                    text: "Change allowed:" //"Days before change allowed:"
                    color: "#e3dbdb"
                    font.bold: true
                    font.pixelSize: 15
                    font.family: "Sans"
                }
                MdvTextInput {
                    id: changedAllowed
                    width: 215
                    //text: "changed allowed"
                    //selectByMouse: true
                }

                Text {
                    text: "Change required:" //"Days before change required:"
                    color: "#e3dbdb"
                    font.bold: true
                    font.pixelSize: 15
                    font.family: "Sans"
                }
                MdvTextInput {
                    id: changedRequired
                    width: 215
                    //text: "changed required"
                    //selectByMouse: true
                }

                Text {
                    text: "Warning change:" //"Days warning before change:"
                    color: "#e3dbdb"
                    font.bold: true
                    font.pixelSize: 15
                    font.family: "Sans"
                }
                MdvTextInput {
                    id: warningChange
                    width: 215
                    //text: "warning change"
                    //selectByMouse: true
                }

                Text {
                    text: "Account inactive:" //"Days before account inactive:"
                    color: "#e3dbdb"
                    font.bold: true
                    font.pixelSize: 15
                    font.family: "Sans"
                }
                MdvTextInput {
                    id: accountInactive
                    width: 215
                    //text: "account inactive"
                    //selectByMouse: true
                }

                Text {
                    text: "Last changed:"//"User last changed password on:"
                    color: "#e3dbdb"
                    font.bold: true
                    font.pixelSize: 15
                    font.family: "Sans"
                }
                Text {
                    text: "Sun Dec 26 2010"
                }

                // Groups *****************************************************
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
                // listViewGroup
                //ListView {
                //   id: listViewGroup
                //    width: content.width
                //    height: content.height
                //    model: groupsModel
                //    delegate: groupDelegate
                //    highlight: Rectangle { color: "steelblue" }
                //    highlightFollowsCurrentItem: true
                    //header: listViewHeader
                    //focus: true
               // }
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
                MdvTextInput {
                    id: groupName
                    width: 215
                    //text: "group name"
                    //focus: true
                    //selectByMouse: true
                }
            }
        }
    }

    /**
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
    **/

    Component {
        id: listViewHeader
        //ButtonGroup {
        //    width: col.width
        //    height: col.height
            Column {
                id: col
                Row {
                    spacing: 10
                    anchors.horizontalCenter:  parent.horizontalCenter
                    MdvButton {
                        width: (listView.width / 2) - 5 //Row spacing
                        text: "Users"
                        //checkable: true
                        //checked: true
                        MouseArea {
                            anchors.fill: parent
                            onClicked: {
                                listView.model = usersModel
                                listView.delegate = userDelegate
                                groupForm.visible = false
                                contentFlick.contentHeight = userForm.height
                                userForm.visible = true
                                deleteButton.opacity = 0.2
                                //addButton.source = "images/list-add-user.png"
                                //editButton.source ="images/user-properties.png"
                                //deleteButton.source = "images/list-remove-user.png"
                            }
                        }
                    }
                    MdvButton {
                        text: "Groups"
                        width: (listView.width / 2) - 5 //Row spacing
                        //checkable: true
                        MouseArea {
                            anchors.fill: parent
                            onClicked: {
                                listView.model = groupsModel
                                listView.delegate = groupDelegate
                                userForm.visible = false
                                contentFlick.contentHeight = groupForm.height
                                groupForm.visible = true
                                deleteButton.opacity = 0.2
                                //addButton.source = "images/user-group-new.png"
                                //editButton.source ="images/user-group-properties.png"
                                //deleteButton.source = "images/user-group-delete.png"
                            }
                        }
                    }
                }
                MdvTextInput {
                    id: searchBox
                    width: listView.width
                    height: 22
                    hint: "Search"
                    //leftIconSource: "images/system-search.png";
                    //onLeftIconClicked: searchBox.hint = "Searching...";
                    //rightIconSource: "images/edit-delete.png";
                    //onRightIconClicked: searchBox.hint = "Search";
                }
            }
        //}
    }

    ListModel {
        id: usersModel
        ListElement {
            username: "wiliam"
            fullname: "Wiliam Souza"
            uid: "500"
            login_shell: "/bin/sh"
            home_directory: "/home/foo"
        }
        ListElement {
            username: "paula"
            fullname: "Ana Paula"
            uid: "501"
            login_shell: "/bin/sh"
            home_directory: "/home/foo"
        }
        ListElement {
            username: "caio"
            fullname: "Caio Eduardo"
            uid: "502"
            login_shell: "/bin/sh"
            home_directory: "/home/foo"
        }
        ListElement {
            username: "Julia"
            fullname: "Ana Julia"
            uid: "503"
            login_shell: "/bin/sh"
            home_directory: "/home/foo"
        }
        ListElement {
            username: "john"
            fullname: "John Doe"
            uid: "666"
            login_shell: "/bin/sh"
            home_directory: "/home/foo"
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
                        text: uid //model.user.uid
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
                                //id: userName
                                text: username //model.user.username
                                color: "#483737"
                                font.bold: true
                                font.pixelSize: 16
                                font.family: "Sans"
                            },
                            Text {
                                //id: fullName
                                text: fullname //model.user.fullname
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
                    console.log("Clicked")
                    listView.currentIndex = index
                    fullName.text = fullname //model.user.fullname
                    userName.text = username //model.user.username
                    loginShell.text = login_shell //model.user.login_shell
                    homeDirectory.text = home_directory //model.user.home_directory
                    deleteButton.opacity = 1

                    // keep this two line at en
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
            gid: "1000"
        }

        ListElement {
            groupname: "paula"
            members: "paula"
            gid: "503"
        }

        ListElement {
            groupname: "caio"
            members: "caio"
            gid: "501"
        }

        ListElement {
            groupname: "Julia"
            members: "julia"
            gid: "502"
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
                        text: gid //model.user.uid
                        color: "#d45500"
                        font.bold: true
                        font.pixelSize: 16
                        font.family: "Sans"
                    },
                    Column { //
                        anchors.verticalCenter: parent.verticalCenter
                        children: [
                            Text {
                                //id: groupName
                                text: groupname
                                color: "#483737"
                                font.bold: true
                                font.pixelSize: 16
                                font.family: "Sans"
                            }
                        ]
                    } //
                ]
            }
            MouseArea {
                anchors.fill: parent
                onClicked: {
                    console.log("Clicked")
                    listView.currentIndex = index
                    groupName.text = groupname
                    deleteButton.opacity = 1

                    // keep this two line at end
                    userForm.visible = false
                    groupForm.visible = true
                }
            }
        }
    }
}
