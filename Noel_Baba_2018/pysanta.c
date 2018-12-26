// pysanta.c
#include <Python.h>
#include <math.h>
#include <stdlib.h>

#define n_asal 17802

// Bu üç array data.c dosyasında yazılı.
extern double x[];
extern double y[];
extern unsigned int asalsehirler[];

inline double mesafe(long onceki, long yeni)
{
    double dx, dy;
    dx = x[yeni] - x[onceki];
    dy = y[yeni] - y[onceki];
    return sqrt(dx*dx+dy*dy);
}

int compareints (const void * a, const void * b)
{
  return ( *(int*)a - *(int*)b );
}

static PyObject* toplam_mesafe(PyObject* self, PyObject* args)
{
    PyObject *yol;
    long onceki, yeni;
    int *item;
    double m;
    double toplam = 0;
    
    if (!PyArg_ParseTuple(args, "O", &yol))
        return NULL;
    
    Py_ssize_t len = PyList_Size(yol);
	
    onceki = PyLong_AsLong(PyList_GetItem(yol, 0));
    
	for (int adim=1; adim<len; adim++) {
        
		yeni = PyLong_AsLong(PyList_GetItem(yol, adim));
        
        m = mesafe(onceki, yeni);
        
        if (adim%10==0) { // On adımda bir bak: Başlangıç şehri asal mı?
            item = (int*) bsearch (&onceki, asalsehirler, n_asal,
                               sizeof (unsigned int), compareints);
            // Asallar arasında bulunmadıysa mesafeyi %10 arttır.
            if (item==NULL) m *= 1.1;
        }
        
        toplam += m;
        onceki = yeni;
	}	
    return Py_BuildValue("f", toplam);
}

static PyMethodDef SantaMethods[] =
{
     {"toplam_mesafe", toplam_mesafe, METH_VARARGS, "Belli bir turun katettiği toplam mesafeyi verir."},
     {NULL, NULL, 0, NULL}
};

static struct PyModuleDef Santa_Module = {  
    PyModuleDef_HEAD_INIT,
    "santa",     // Python'un gordugu modul ismi.
    "Gezgin Santa Problemi modulu.", // modul belgeleme dizesi
    -1,
    SantaMethods
};

PyMODINIT_FUNC PyInit_santa(void)
{
     return PyModule_Create(&Santa_Module);
}
