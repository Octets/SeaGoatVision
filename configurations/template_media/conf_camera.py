#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

from SeaGoatVision.server.media.implementation.cameraManta import CameraManta


class ConfCamera:

    def __init__(self):
        self.media = CameraManta
        self.name = "Camera"
        self.no = -1
        self.default_fps = 30
