#include "Main.h"

int main() {
    string token("You token");

    const string FilePath = "Some data.backup";
    const string MimeType = "";

    Bot bot(token);

    ReplyKeyboardMarkup::Ptr keyboardOneCol(new ReplyKeyboardMarkup);
    createOneColumnKeyboard({ "ReadyToScan", "SMBVulnerable" }, keyboardOneCol);
    bot.getEvents().onCommand("start", [&bot, &keyboardOneCol](Message::Ptr message) {
        bot.getApi().sendMessage(message->chat->id, "Hi! I'm SMBbot, view info from db, my options:\n/start for PostgreSQL keyboard map\n/backup for latest backup", false, 0, keyboardOneCol);
        });
    bot.getEvents().onCommand("backup", [&bot, &FilePath, &MimeType](Message::Ptr message) {
        bot.getApi().sendDocument(message->chat->id, InputFile::fromFile(FilePath, MimeType));
        });
    bot.getEvents().onAnyMessage([&bot](Message::Ptr message) {
        printf("%s wrote %s\n", message->chat->firstName.c_str(), message->text.c_str());

        if (StringTools::startsWith(message->text, "/start")) { return; }
       
        // Create validating message
        std::string textFromUser{ message->text };
        std::string valid_text_ready{ "ReadyToScan" };
        std::string valid_text_smb{ "SMBVulnerable" };

        if (textFromUser == valid_text_ready) {
            bot.getApi().sendMessage(message->chat->id, "Correct passphrase! " + textFromUser);
        }
        else if (textFromUser == valid_text_smb) {
            bot.getApi().sendMessage(message->chat->id, "Correct passphrase!" + textFromUser);
        }
        
        });

    signal(SIGINT, [](int s) { printf("SIGINT got\n"); exit(0); });

    try {
        printf("Bot username: %s\n", bot.getApi().getMe()->username.c_str());

        bot.getApi().deleteWebhook();

        TgLongPoll longPoll(bot);
        while (true) {
            longPoll.start();
        }
    }
    catch (exception& e) { printf("error: %s\n", e.what()); }

    return 0;
}