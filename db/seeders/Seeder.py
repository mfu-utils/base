from App.Core.Abstract.AbstractSeeder import AbstractSeeder
#: BUILD_TYPE:!server
from db.seeders.Client.LanguagesSeeder import LanguagesSeeder
from db.seeders.Client.ScanTypeSeeder import ScanTypeSeeder
#: END:BUILD_TYPE:!server


class Seeder(AbstractSeeder):
    def run(self):
        self._group([
            #: BUILD_TYPE:!server
            ScanTypeSeeder,
            LanguagesSeeder,
            #: END:BUILD_TYPE:!server
        ])
