/****************************************************************************
** Meta object code from reading C++ file 'qstyleitem.h'
**
** Created: Fri Mar 25 04:41:33 2011
**      by: The Qt Meta Object Compiler version 62 (Qt 4.7.2)
**
** WARNING! All changes made in this file will be lost!
*****************************************************************************/

#include "../qstyleitem.h"
#if !defined(Q_MOC_OUTPUT_REVISION)
#error "The header file 'qstyleitem.h' doesn't include <QObject>."
#elif Q_MOC_OUTPUT_REVISION != 62
#error "This file was generated using the moc from 4.7.2. It"
#error "cannot be used with the include files from this version of Qt."
#error "(The moc has changed too much.)"
#endif

QT_BEGIN_MOC_NAMESPACE
static const uint qt_meta_data_QStyleItem[] = {

 // content:
       5,       // revision
       0,       // classname
       0,    0, // classinfo
      21,   14, // methods
      17,  119, // properties
       0,    0, // enums/sets
       0,    0, // constructors
       0,       // flags
      18,       // signalCount

 // signals: signature, parameters, type, tag, flags
      12,   11,   11,   11, 0x05,
      33,   11,   11,   11, 0x05,
      47,   11,   11,   11, 0x05,
      63,   11,   11,   11, 0x05,
      79,   11,   11,   11, 0x05,
      95,   11,   11,   11, 0x05,
     112,   11,   11,   11, 0x05,
     130,   11,   11,   11, 0x05,
     145,   11,   11,   11, 0x05,
     157,   11,   11,   11, 0x05,
     172,   11,   11,   11, 0x05,
     192,   11,   11,   11, 0x05,
     209,   11,   11,   11, 0x05,
     226,   11,   11,   11, 0x05,
     241,   11,   11,   11, 0x05,
     264,   11,   11,   11, 0x05,
     278,   11,   11,   11, 0x05,
     293,   11,   11,   11, 0x05,

 // slots: signature, parameters, type, tag, flags
     310,   11,  306,   11, 0x0a,
     340,   11,  331,   11, 0x0a,
     378,  365,  359,   11, 0x0a,

 // properties: name, type, flags
     409,  404, 0x01495103,
     416,  404, 0x01495103,
     423,  404, 0x01495103,
     430,  404, 0x01495103,
     438,  404, 0x01495103,
     447,  404, 0x01495103,
     453,  404, 0x01495103,
     456,  404, 0x01495103,
     462,  404, 0x01495103,
     481,  473, 0x0a495103,
     493,  473, 0x0a495103,
     498,  473, 0x0a495103,
     512,  473, 0x0a495103,
     517,  473, 0x0a495001,
     523,  306, 0x02495103,
     531,  306, 0x02495103,
     539,  306, 0x02495103,

 // properties: notify_signal_id
       2,
       3,
       4,
       5,
       6,
       7,
       8,
       9,
      10,
       0,
       1,
      14,
      15,
      16,
      11,
      12,
      13,

       0        // eod
};

static const char qt_meta_stringdata_QStyleItem[] = {
    "QStyleItem\0\0elementTypeChanged()\0"
    "textChanged()\0sunkenChanged()\0"
    "raisedChanged()\0activeChanged()\0"
    "enabledChanged()\0selectedChanged()\0"
    "focusChanged()\0onChanged()\0hoverChanged()\0"
    "horizontalChanged()\0minimumChanged()\0"
    "maximumChanged()\0valueChanged()\0"
    "activeControlChanged()\0infoChanged()\0"
    "styleChanged()\0updateItem()\0int\0"
    "pixelMetric(QString)\0QVariant\0"
    "styleHint(QString)\0QSize\0width,height\0"
    "sizeFromContents(int,int)\0bool\0sunken\0"
    "raised\0active\0enabled\0selected\0focus\0"
    "on\0hover\0horizontal\0QString\0elementType\0"
    "text\0activeControl\0info\0style\0minimum\0"
    "maximum\0value\0"
};

const QMetaObject QStyleItem::staticMetaObject = {
    { &QObject::staticMetaObject, qt_meta_stringdata_QStyleItem,
      qt_meta_data_QStyleItem, 0 }
};

#ifdef Q_NO_DATA_RELOCATION
const QMetaObject &QStyleItem::getStaticMetaObject() { return staticMetaObject; }
#endif //Q_NO_DATA_RELOCATION

const QMetaObject *QStyleItem::metaObject() const
{
    return QObject::d_ptr->metaObject ? QObject::d_ptr->metaObject : &staticMetaObject;
}

void *QStyleItem::qt_metacast(const char *_clname)
{
    if (!_clname) return 0;
    if (!strcmp(_clname, qt_meta_stringdata_QStyleItem))
        return static_cast<void*>(const_cast< QStyleItem*>(this));
    return QObject::qt_metacast(_clname);
}

int QStyleItem::qt_metacall(QMetaObject::Call _c, int _id, void **_a)
{
    _id = QObject::qt_metacall(_c, _id, _a);
    if (_id < 0)
        return _id;
    if (_c == QMetaObject::InvokeMetaMethod) {
        switch (_id) {
        case 0: elementTypeChanged(); break;
        case 1: textChanged(); break;
        case 2: sunkenChanged(); break;
        case 3: raisedChanged(); break;
        case 4: activeChanged(); break;
        case 5: enabledChanged(); break;
        case 6: selectedChanged(); break;
        case 7: focusChanged(); break;
        case 8: onChanged(); break;
        case 9: hoverChanged(); break;
        case 10: horizontalChanged(); break;
        case 11: minimumChanged(); break;
        case 12: maximumChanged(); break;
        case 13: valueChanged(); break;
        case 14: activeControlChanged(); break;
        case 15: infoChanged(); break;
        case 16: styleChanged(); break;
        case 17: updateItem(); break;
        case 18: { int _r = pixelMetric((*reinterpret_cast< const QString(*)>(_a[1])));
            if (_a[0]) *reinterpret_cast< int*>(_a[0]) = _r; }  break;
        case 19: { QVariant _r = styleHint((*reinterpret_cast< const QString(*)>(_a[1])));
            if (_a[0]) *reinterpret_cast< QVariant*>(_a[0]) = _r; }  break;
        case 20: { QSize _r = sizeFromContents((*reinterpret_cast< int(*)>(_a[1])),(*reinterpret_cast< int(*)>(_a[2])));
            if (_a[0]) *reinterpret_cast< QSize*>(_a[0]) = _r; }  break;
        default: ;
        }
        _id -= 21;
    }
#ifndef QT_NO_PROPERTIES
      else if (_c == QMetaObject::ReadProperty) {
        void *_v = _a[0];
        switch (_id) {
        case 0: *reinterpret_cast< bool*>(_v) = sunken(); break;
        case 1: *reinterpret_cast< bool*>(_v) = raised(); break;
        case 2: *reinterpret_cast< bool*>(_v) = active(); break;
        case 3: *reinterpret_cast< bool*>(_v) = enabled(); break;
        case 4: *reinterpret_cast< bool*>(_v) = selected(); break;
        case 5: *reinterpret_cast< bool*>(_v) = focus(); break;
        case 6: *reinterpret_cast< bool*>(_v) = on(); break;
        case 7: *reinterpret_cast< bool*>(_v) = hover(); break;
        case 8: *reinterpret_cast< bool*>(_v) = horizontal(); break;
        case 9: *reinterpret_cast< QString*>(_v) = elementType(); break;
        case 10: *reinterpret_cast< QString*>(_v) = text(); break;
        case 11: *reinterpret_cast< QString*>(_v) = activeControl(); break;
        case 12: *reinterpret_cast< QString*>(_v) = info(); break;
        case 13: *reinterpret_cast< QString*>(_v) = style(); break;
        case 14: *reinterpret_cast< int*>(_v) = minimum(); break;
        case 15: *reinterpret_cast< int*>(_v) = maximum(); break;
        case 16: *reinterpret_cast< int*>(_v) = value(); break;
        }
        _id -= 17;
    } else if (_c == QMetaObject::WriteProperty) {
        void *_v = _a[0];
        switch (_id) {
        case 0: setSunken(*reinterpret_cast< bool*>(_v)); break;
        case 1: setRaised(*reinterpret_cast< bool*>(_v)); break;
        case 2: setActive(*reinterpret_cast< bool*>(_v)); break;
        case 3: setEnabled(*reinterpret_cast< bool*>(_v)); break;
        case 4: setSelected(*reinterpret_cast< bool*>(_v)); break;
        case 5: setFocus(*reinterpret_cast< bool*>(_v)); break;
        case 6: setOn(*reinterpret_cast< bool*>(_v)); break;
        case 7: setHover(*reinterpret_cast< bool*>(_v)); break;
        case 8: setHorizontal(*reinterpret_cast< bool*>(_v)); break;
        case 9: setElementType(*reinterpret_cast< QString*>(_v)); break;
        case 10: setText(*reinterpret_cast< QString*>(_v)); break;
        case 11: setActiveControl(*reinterpret_cast< QString*>(_v)); break;
        case 12: setInfo(*reinterpret_cast< QString*>(_v)); break;
        case 14: setMinimum(*reinterpret_cast< int*>(_v)); break;
        case 15: setMaximum(*reinterpret_cast< int*>(_v)); break;
        case 16: setValue(*reinterpret_cast< int*>(_v)); break;
        }
        _id -= 17;
    } else if (_c == QMetaObject::ResetProperty) {
        _id -= 17;
    } else if (_c == QMetaObject::QueryPropertyDesignable) {
        _id -= 17;
    } else if (_c == QMetaObject::QueryPropertyScriptable) {
        _id -= 17;
    } else if (_c == QMetaObject::QueryPropertyStored) {
        _id -= 17;
    } else if (_c == QMetaObject::QueryPropertyEditable) {
        _id -= 17;
    } else if (_c == QMetaObject::QueryPropertyUser) {
        _id -= 17;
    }
#endif // QT_NO_PROPERTIES
    return _id;
}

// SIGNAL 0
void QStyleItem::elementTypeChanged()
{
    QMetaObject::activate(this, &staticMetaObject, 0, 0);
}

// SIGNAL 1
void QStyleItem::textChanged()
{
    QMetaObject::activate(this, &staticMetaObject, 1, 0);
}

// SIGNAL 2
void QStyleItem::sunkenChanged()
{
    QMetaObject::activate(this, &staticMetaObject, 2, 0);
}

// SIGNAL 3
void QStyleItem::raisedChanged()
{
    QMetaObject::activate(this, &staticMetaObject, 3, 0);
}

// SIGNAL 4
void QStyleItem::activeChanged()
{
    QMetaObject::activate(this, &staticMetaObject, 4, 0);
}

// SIGNAL 5
void QStyleItem::enabledChanged()
{
    QMetaObject::activate(this, &staticMetaObject, 5, 0);
}

// SIGNAL 6
void QStyleItem::selectedChanged()
{
    QMetaObject::activate(this, &staticMetaObject, 6, 0);
}

// SIGNAL 7
void QStyleItem::focusChanged()
{
    QMetaObject::activate(this, &staticMetaObject, 7, 0);
}

// SIGNAL 8
void QStyleItem::onChanged()
{
    QMetaObject::activate(this, &staticMetaObject, 8, 0);
}

// SIGNAL 9
void QStyleItem::hoverChanged()
{
    QMetaObject::activate(this, &staticMetaObject, 9, 0);
}

// SIGNAL 10
void QStyleItem::horizontalChanged()
{
    QMetaObject::activate(this, &staticMetaObject, 10, 0);
}

// SIGNAL 11
void QStyleItem::minimumChanged()
{
    QMetaObject::activate(this, &staticMetaObject, 11, 0);
}

// SIGNAL 12
void QStyleItem::maximumChanged()
{
    QMetaObject::activate(this, &staticMetaObject, 12, 0);
}

// SIGNAL 13
void QStyleItem::valueChanged()
{
    QMetaObject::activate(this, &staticMetaObject, 13, 0);
}

// SIGNAL 14
void QStyleItem::activeControlChanged()
{
    QMetaObject::activate(this, &staticMetaObject, 14, 0);
}

// SIGNAL 15
void QStyleItem::infoChanged()
{
    QMetaObject::activate(this, &staticMetaObject, 15, 0);
}

// SIGNAL 16
void QStyleItem::styleChanged()
{
    QMetaObject::activate(this, &staticMetaObject, 16, 0);
}

// SIGNAL 17
void QStyleItem::updateItem()
{
    QMetaObject::activate(this, &staticMetaObject, 17, 0);
}
static const uint qt_meta_data_QStyleBackground[] = {

 // content:
       5,       // revision
       0,       // classname
       0,    0, // classinfo
       7,   14, // methods
       1,   49, // properties
       0,    0, // enums/sets
       0,    0, // constructors
       0,       // flags
       1,       // signalCount

 // signals: signature, parameters, type, tag, flags
      18,   17,   17,   17, 0x05,

 // slots: signature, parameters, type, tag, flags
      45,   17,   33,   17, 0x0a,
      59,   53,   17,   17, 0x0a,
      81,   17,   17,   17, 0x0a,
     106,  102,   94,   17, 0x0a,
     146,  129,  123,   17, 0x0a,
     174,  170,   17,   17, 0x0a,

 // properties: name, type, flags
      53,   33, 0x0049510b,

 // properties: notify_signal_id
       0,

       0        // eod
};

static const char qt_meta_stringdata_QStyleBackground[] = {
    "QStyleBackground\0\0styleChanged()\0"
    "QStyleItem*\0style()\0style\0"
    "setStyle(QStyleItem*)\0updateItem()\0"
    "QString\0x,y\0hitTest(int,int)\0QRect\0"
    "subcontrolString\0subControlRect(QString)\0"
    "str\0showToolTip(QString)\0"
};

const QMetaObject QStyleBackground::staticMetaObject = {
    { &QDeclarativeItem::staticMetaObject, qt_meta_stringdata_QStyleBackground,
      qt_meta_data_QStyleBackground, 0 }
};

#ifdef Q_NO_DATA_RELOCATION
const QMetaObject &QStyleBackground::getStaticMetaObject() { return staticMetaObject; }
#endif //Q_NO_DATA_RELOCATION

const QMetaObject *QStyleBackground::metaObject() const
{
    return QObject::d_ptr->metaObject ? QObject::d_ptr->metaObject : &staticMetaObject;
}

void *QStyleBackground::qt_metacast(const char *_clname)
{
    if (!_clname) return 0;
    if (!strcmp(_clname, qt_meta_stringdata_QStyleBackground))
        return static_cast<void*>(const_cast< QStyleBackground*>(this));
    return QDeclarativeItem::qt_metacast(_clname);
}

int QStyleBackground::qt_metacall(QMetaObject::Call _c, int _id, void **_a)
{
    _id = QDeclarativeItem::qt_metacall(_c, _id, _a);
    if (_id < 0)
        return _id;
    if (_c == QMetaObject::InvokeMetaMethod) {
        switch (_id) {
        case 0: styleChanged(); break;
        case 1: { QStyleItem* _r = style();
            if (_a[0]) *reinterpret_cast< QStyleItem**>(_a[0]) = _r; }  break;
        case 2: setStyle((*reinterpret_cast< QStyleItem*(*)>(_a[1]))); break;
        case 3: updateItem(); break;
        case 4: { QString _r = hitTest((*reinterpret_cast< int(*)>(_a[1])),(*reinterpret_cast< int(*)>(_a[2])));
            if (_a[0]) *reinterpret_cast< QString*>(_a[0]) = _r; }  break;
        case 5: { QRect _r = subControlRect((*reinterpret_cast< const QString(*)>(_a[1])));
            if (_a[0]) *reinterpret_cast< QRect*>(_a[0]) = _r; }  break;
        case 6: showToolTip((*reinterpret_cast< const QString(*)>(_a[1]))); break;
        default: ;
        }
        _id -= 7;
    }
#ifndef QT_NO_PROPERTIES
      else if (_c == QMetaObject::ReadProperty) {
        void *_v = _a[0];
        switch (_id) {
        case 0: *reinterpret_cast< QStyleItem**>(_v) = style(); break;
        }
        _id -= 1;
    } else if (_c == QMetaObject::WriteProperty) {
        void *_v = _a[0];
        switch (_id) {
        case 0: setStyle(*reinterpret_cast< QStyleItem**>(_v)); break;
        }
        _id -= 1;
    } else if (_c == QMetaObject::ResetProperty) {
        _id -= 1;
    } else if (_c == QMetaObject::QueryPropertyDesignable) {
        _id -= 1;
    } else if (_c == QMetaObject::QueryPropertyScriptable) {
        _id -= 1;
    } else if (_c == QMetaObject::QueryPropertyStored) {
        _id -= 1;
    } else if (_c == QMetaObject::QueryPropertyEditable) {
        _id -= 1;
    } else if (_c == QMetaObject::QueryPropertyUser) {
        _id -= 1;
    }
#endif // QT_NO_PROPERTIES
    return _id;
}

// SIGNAL 0
void QStyleBackground::styleChanged()
{
    QMetaObject::activate(this, &staticMetaObject, 0, 0);
}
QT_END_MOC_NAMESPACE
