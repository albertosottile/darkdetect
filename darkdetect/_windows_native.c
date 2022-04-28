#pragma comment(lib, "Advapi32.lib")

#include <Python.h>
#include <windows.h>

static PyObject *method_listener(PyObject *self, PyObject *args) {
    PyObject *cb;

    if (!PyArg_ParseTuple(args, "O", &cb) || !PyCallable_Check(cb)) {
        PyErr_SetString(PyExc_TypeError, "A callable is required");
        return NULL;
    }

    HKEY hKey;
    RegOpenKeyExA(HKEY_CURRENT_USER, "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize", 0, KEY_NOTIFY | KEY_READ, &hKey);
    DWORD dwSize = sizeof(DWORD);
    DWORD queryValueLast;
    DWORD queryValue;
    RegQueryValueExA(hKey, "AppsUseLightTheme", NULL, NULL, (LPBYTE)&queryValueLast, &dwSize);
    while (TRUE) {
        Py_BEGIN_ALLOW_THREADS
        RegNotifyChangeKeyValue(hKey, TRUE, REG_NOTIFY_CHANGE_LAST_SET, NULL, FALSE);
        Py_END_ALLOW_THREADS
        RegQueryValueExA(hKey, "AppsUseLightTheme", NULL, NULL, (LPBYTE)&queryValue, &dwSize);
        if (queryValueLast != queryValue) {
            queryValueLast = queryValue;
            PyObject *rv = PyObject_CallFunction(cb, "s", queryValue ? "Light" : "Dark");
            Py_CLEAR(rv);
        }
    }
}

static PyMethodDef FputsMethods[] = {
    {"listener", method_listener, METH_VARARGS, "Listen for theme switch and run callback function."},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef native_module = {
    PyModuleDef_HEAD_INIT,
    "_windows_native",
    "Native functions for dark mode detection on Windows.",
    -1,
    FputsMethods
};

PyMODINIT_FUNC PyInit__windows_native(void) {
    return PyModule_Create(&native_module);
}