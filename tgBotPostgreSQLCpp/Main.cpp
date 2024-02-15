#include "Main.h"


int main() {
    SetConsoleCP(1251);
    SetConsoleOutputCP(1251);

    string token("");

    const string FilePathBackup = "SMBHosts.backup";
    const string FilePathRanges = "./ranges/RUSSIA.txt";
    const string MimeType = "";

    const int SEARCH = 1;
    const int VIEW = 2;
    const int COUNT = 3;
    const int INFO = 4;
    const int ABOUT = 5;

    Bot bot(token);

    ReplyKeyboardMarkup::Ptr keyboardWithLayout(new ReplyKeyboardMarkup);
    createKeyboard({
        {"SEARCH", "VIEW"},
        {"COUNT"},
        {"INFO", "ABOUT"}
        }, keyboardWithLayout);

    bot.getEvents().onCommand("start", [&bot](Message::Ptr message) {
        bot.getApi().sendMessage(message->chat->id, "[SMB_AUTOMATION]\nHi! I use saved data from the database.\n"
                                                    "Used to check data and authorization: masscan, ruby, python. My basic options:\n"
                                                    "/keymap for PostgreSQL keyboard map\n/backup for latest backup\n/ranges to view list scan ranges", false, 0);
        });
    bot.getEvents().onCommand("backup", [&bot, &FilePathBackup, &MimeType](Message::Ptr message) {
        bot.getApi().sendDocument(message->chat->id, InputFile::fromFile(FilePathBackup, MimeType));
        });
    bot.getEvents().onCommand("ranges", [&bot, &FilePathRanges, &MimeType](Message::Ptr message) {
        bot.getApi().sendDocument(message->chat->id, InputFile::fromFile(FilePathRanges, MimeType));
        });
    bot.getEvents().onCommand("keymap", [&bot, &keyboardWithLayout](Message::Ptr message) {
        bot.getApi().sendMessage(message->chat->id, "SEARCH - Search by folder names\nExample: SEARCH Photos\n\n"
                                                    "VIEW - Will output all data from the db\nExample: VIEW\n\n"
                                                    "COUNT - Folder repeat counter\nExample: COUNT\n\n"
                                                    "INFO - db info\nExample: INFO\n\n"
                                                    "ABOUT - Current info vers, time\nExample: ABOUT", false, 0, keyboardWithLayout);
        });

    vector<BotCommand::Ptr> commands;
    BotCommand::Ptr cmdArray(new BotCommand);
    cmdArray->command = "/keymap";
    cmdArray->description = "PostgreSQL keyboard map";

    commands.push_back(cmdArray);

    cmdArray = BotCommand::Ptr(new BotCommand);
    cmdArray->command = "/backup";
    cmdArray->description = "Get latest backup only admins";
    commands.push_back(cmdArray);

    cmdArray = BotCommand::Ptr(new BotCommand);
    cmdArray->command = "/ranges";
    cmdArray->description = "View list scan ranges";
    commands.push_back(cmdArray);

    bot.getApi().setMyCommands(commands);

    vector<BotCommand::Ptr> vectCmd;
    vectCmd = bot.getApi().getMyCommands();

    for (std::vector<BotCommand::Ptr>::iterator it = vectCmd.begin(); it != vectCmd.end(); ++it) {
        printf("cmd: %s -> %s\r", (*it)->command.c_str(), (*it)->description.c_str());
    }

    bot.getEvents().onAnyMessage([&bot](Message::Ptr message) {
        std::unordered_map<std::string, int> mapping;
        std::string messageText{ message->text };

        mapping["SEARCH"] = SEARCH;
        mapping["VIEW"] = VIEW;
        mapping["COUNT"] = COUNT;
        mapping["INFO"] = INFO;
        mapping["ABOUT"] = ABOUT;

        currentTimeValue();
        printf(" %s wrote %s\n", message->chat->firstName.c_str(), message->text.c_str());

        std::string textFromUser{ messageText };

        if (StringTools::startsWith(messageText, "/start")) { return; }

        switch (mapping[messageText]) {
        case SEARCH:
            bot.getApi().sendMessage(message->chat->id, "Case SEARCH: " + messageText);
            break;
        case VIEW:
            bot.getApi().sendMessage(message->chat->id, "Case VIEW: " + messageText);
            break;
        case COUNT:
            bot.getApi().sendMessage(message->chat->id, "Case COUNT: " + messageText);
            break;
        case INFO:
            bot.getApi().sendMessage(message->chat->id, "Case INFO: " + messageText);
            break;
        case ABOUT:
            bot.getApi().sendMessage(message->chat->id, "Bot based on c++, using PostgreSQL data view\ngit:" 
                "https://github.com/sxfour/smb_automation");
            break;
        default:
            break;
        }
        
        });

    signal(SIGINT, [](int s) {
        currentTimeValue();
        printf(" SIGINT got\n");
        exit(0);
        }
    );

    try {
        currentTimeValue();
        printf(" Bot username: %s\n", bot.getApi().getMe()->username.c_str());

        bot.getApi().deleteWebhook();

        TgLongPoll longPoll(bot);
        while (true) {
            longPoll.start();
        }
    }
    catch (exception& e) {
        currentTimeValue();
        printf(" error: %s\n", e.what());
    }

    return 0;
}