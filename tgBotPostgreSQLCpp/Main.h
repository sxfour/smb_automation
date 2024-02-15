#pragma once

#include <csignal>
#include <cstdio>
#include <cstdlib>
#include <exception>
#include <string>
#include <chrono>
#include <format>
#include <tgbot/tgbot.h>
#include <Windows.h>

using namespace std;
using namespace TgBot;

void createOneColumnKeyboard(const vector<string>& buttonStrings, ReplyKeyboardMarkup::Ptr& kb)
{
    for (size_t i = 0; i < buttonStrings.size(); ++i) {
        vector<KeyboardButton::Ptr> row;
        KeyboardButton::Ptr button(new KeyboardButton);
        button->text = buttonStrings[i];
        row.push_back(button);
        kb->keyboard.push_back(row);
    }
}

void createKeyboard(const vector<vector<string>>& buttonLayout, ReplyKeyboardMarkup::Ptr& kb)
{
    for (size_t i = 0; i < buttonLayout.size(); ++i) {
        vector<KeyboardButton::Ptr> row;
        for (size_t j = 0; j < buttonLayout[i].size(); ++j) {
            KeyboardButton::Ptr button(new KeyboardButton);
            button->text = buttonLayout[i][j];
            row.push_back(button);
        }
        kb->keyboard.push_back(row);
    }
}

void currentTimeValue() {
    const auto now = std::chrono::system_clock::now();

    std::cout << std::format("[{:%d-%m-%Y %H:%M:%OS}]", now);
}