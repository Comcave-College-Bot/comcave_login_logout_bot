#include <windows.h>
#include <string>

int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance,
    LPSTR lpCmdLine, int nCmdShow)
{
    STARTUPINFOW si = {sizeof(STARTUPINFOW)};
    PROCESS_INFORMATION pi;

    WCHAR cmd[] = L"pythonw gui.py --redirect";

    // GUI im Hintergrund starten
    CreateProcessW(NULL, cmd,
        NULL, NULL, FALSE,
        CREATE_NO_WINDOW,
        NULL, NULL, &si, &pi);

    // Handles schließen
    CloseHandle(pi.hProcess);
    CloseHandle(pi.hThread);

    return 0;
}