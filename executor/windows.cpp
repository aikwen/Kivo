#include <windows.h>
#pragma comment(lib, "User32.lib")

#include <filesystem>
#include <string>
#include <vector>


static void show_error(
    const std::wstring& message
) {
    MessageBoxW(
        nullptr,
        message.c_str(),
        L"Kivo",
        MB_OK | MB_ICONERROR
    );
}


int WINAPI wWinMain(
    HINSTANCE,
    HINSTANCE,
    PWSTR,
    int
) {
    wchar_t local_app_data[MAX_PATH];

    DWORD length = GetEnvironmentVariableW(
        L"LOCALAPPDATA",
        local_app_data,
        MAX_PATH
    );

    if (length == 0 || length >= MAX_PATH) {
        show_error(
            L"Failed to locate LOCALAPPDATA."
        );
        return 1;
    }

    std::filesystem::path config_path =
        std::filesystem::path(local_app_data)
        / L"Kivo"
        / L"config.ini";

    wchar_t python_path[MAX_PATH];

    DWORD python_length = GetPrivateProfileStringW(
        L"runtime",
        L"python",
        L"",
        python_path,
        MAX_PATH,
        config_path.c_str()
    );

    if (python_length == 0) {
        show_error(
            L"Kivo is not configured.\n\n"
            L"Run `kivo setup` first."
        );
        return 2;
    }

    std::filesystem::path executable_path(
        python_path
    );

    if (!std::filesystem::exists(executable_path)) {
        show_error(
            L"The configured Python interpreter "
            L"does not exist.\n\n"
            L"Run `kivo setup` again."
        );
        return 3;
    }

    std::filesystem::path pythonw_path =
        executable_path.parent_path()
        / L"pythonw.exe";

    if (std::filesystem::exists(pythonw_path)) {
        executable_path = pythonw_path;
    }

    std::wstring command_line =
        L"\"" + executable_path.wstring()
        + L"\" -m kivo.main";

    std::vector<wchar_t> command_buffer(
        command_line.begin(),
        command_line.end()
    );
    command_buffer.push_back(L'\0');

    STARTUPINFOW startup_info{};
    startup_info.cb = sizeof(startup_info);

    PROCESS_INFORMATION process_info{};

    BOOL created = CreateProcessW(
        executable_path.c_str(),
        command_buffer.data(),
        nullptr,
        nullptr,
        FALSE,
        0,
        nullptr,
        nullptr,
        &startup_info,
        &process_info
    );

    if (!created) {
        DWORD error = GetLastError();

        show_error(
            L"Failed to start Kivo.\n\n"
            L"Windows error code: "
            + std::to_wstring(error)
        );

        return 4;
    }

    CloseHandle(process_info.hThread);
    CloseHandle(process_info.hProcess);

    return 0;
}