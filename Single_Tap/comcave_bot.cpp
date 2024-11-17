#include <windows.h>
#include <string>

int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance,
    LPSTR lpCmdLine, int nCmdShow)
{
    STARTUPINFOW si = {sizeof(STARTUPINFOW)};
    PROCESS_INFORMATION pi;

    // Erst requirements installieren
    WCHAR install_cmd[] = L"python -c \"import subprocess, sys; subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)\"";

    CreateProcessW(NULL, install_cmd,
        NULL, NULL, FALSE,
        CREATE_NO_WINDOW,
        NULL, NULL, &si, &pi);

    // Warten bis Installation abgeschlossen
    WaitForSingleObject(pi.hProcess, INFINITE);
    CloseHandle(pi.hProcess);
    CloseHandle(pi.hThread);

    // Dann GUI starten
    WCHAR cmd[] = L"pythonw gui.py --redirect";

    CreateProcessW(NULL, cmd,
        NULL, NULL, FALSE,
        CREATE_NO_WINDOW,
        NULL, NULL, &si, &pi);

    CloseHandle(pi.hProcess);
    CloseHandle(pi.hThread);

    return 0;
} 