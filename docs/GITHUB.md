# Lista de publicación en GitHub

No se deben afirmar commits, Issues, pull requests o releases que no se hayan creado realmente. El equipo debe hacer estos pasos en su repositorio.

## 1. Crear el repositorio
1. En GitHub, cree un repositorio público llamado `sistema-gestion-comercial`.
2. No agregue una licencia o README desde la web si va a subir esta carpeta completa con su propio README (para evitar conflictos iniciales).
3. Descomprima el ZIP y abra una terminal en la carpeta que contiene `README.md`.

## 2. Primer envío
```bash
git init
git branch -M main
git add README.md .gitignore src tests docs data/.gitkeep
git commit -m "Crear estructura inicial del sistema comercial"
git remote add origin https://github.com/USUARIO/sistema-gestion-comercial.git
git push -u origin main
```
Reemplace `USUARIO` por el usuario real del equipo. No suba datos de clientes o ventas reales.

## 3. Ocho commits significativos
Distribuya los cambios en commits que reflejen trabajo real del equipo. Ejemplos de mensajes, solo si corresponden a cambios hechos:
1. `Crear estructura inicial del sistema comercial`
2. `Implementar registro y consulta de productos`
3. `Agregar gestión básica de clientes`
4. `Implementar ventas con cálculo de IVA`
5. `Registrar movimientos de inventario`
6. `Agregar reportes estadísticos desde JSON`
7. `Documentar procesos y manuales del sistema`
8. `Agregar pruebas automatizadas y validar flujos`
No cree commits ficticios ni divida artificialmente un solo cambio solo para cumplir el número. Cada integrante debe participar desde su cuenta.

## 4. Rama y pull request
```bash
git checkout -b feature/reportes-estadisticos
```
Realice una mejora real de reportes, pruebe, y después:
```bash
git add src/reportes.py tests docs
git commit -m "Mejorar reportes estadísticos y sus pruebas"
git push -u origin feature/reportes-estadisticos
```
En GitHub, abra un Pull Request desde esa rama hacia `main`, revise los cambios y complete el merge después de la revisión del equipo.

## 5. Issue y release
- Cree un Issue para un problema real detectado y otro para una mejora pendiente, si el requisito pide ambos.
- Después de probar el proyecto integrado, abra **Releases > Draft a new release**, cree la etiqueta `v1.0.0` y describa la versión final.
- Verifique que el README explica cómo ejecutar y probar el sistema.

## 6. Entrega
Copie el enlace público del repositorio y compruebe desde otra sesión o ventana privada que los archivos se puedan ver. Adjunte capturas reales del historial de commits, rama/PR, Issues, release y ejecución del programa.
