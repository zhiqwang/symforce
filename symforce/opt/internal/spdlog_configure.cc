#include <algorithm>
#include <cctype>
#include <cstdlib>

#include <fmt/ranges.h>
#include <spdlog/spdlog.h>

namespace sym {
namespace internal {

class SpdlogConfigurator {
 private:
  SpdlogConfigurator() {
    SetLogLevel();
  }

  void SetLogLevel() const {
    // This is not an owning pointer - it points to the actual location of the string for this
    // environment variable in the process address space.  And this is thread safe, assuming no one
    // modifies SYMFORCE_LOGLEVEL at that location
    // https://stackoverflow.com/a/30476732
    const char* const log_level_cstr = std::getenv("SYMFORCE_LOGLEVEL");

    if (log_level_cstr == nullptr) {
      // getenv returns null if the variable does not exist
      return;
    }

    const std::string log_level_str = log_level_cstr;

    if (log_level_str.empty()) {
      return;
    }

    // Convert to lowercase
    // https://stackoverflow.com/a/313990
    const std::string log_level_str_lower = [&log_level_str]() {
      std::string log_level_str_lower = log_level_str;
      std::transform(log_level_str_lower.begin(), log_level_str_lower.end(),
                     log_level_str_lower.begin(), [](const char c) { return std::tolower(c); });
      return log_level_str_lower;
    }();

    // These should match the python logging levels from
    // https://docs.python.org/3/library/logging.html#logging-levels
    const std::unordered_map<std::string, spdlog::level::level_enum> level_for_string = {
        {"debug", spdlog::level::debug},       {"info", spdlog::level::info},
        {"warning", spdlog::level::warn},      {"error", spdlog::level::err},
        {"critical", spdlog::level::critical},
    };

    const auto maybe_log_level = level_for_string.find(log_level_str_lower);

    if (maybe_log_level == level_for_string.end()) {
      spdlog::error("Invalid log level: \"{}\", keeping current level \"{}\"", log_level_str_lower,
                    spdlog::level::to_string_view(spdlog::get_level()));

      std::vector<std::string> keys;
      std::transform(level_for_string.begin(), level_for_string.end(), std::back_inserter(keys),
                     [](const auto& p) { return p.first; });
      spdlog::error("Allowed values are: {}", keys);
      return;
    }

    spdlog::set_level(maybe_log_level->second);
    spdlog::debug("Set log level to: {}", maybe_log_level->first);
  }

  // Construct a static SpdlogConfigurator, so the constructor runs on process startup
  static SpdlogConfigurator g_spdlog_configurator_;
};

SpdlogConfigurator SpdlogConfigurator::g_spdlog_configurator_{};

}  // namespace internal
}  // namespace sym
