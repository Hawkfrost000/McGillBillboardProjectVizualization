import java.sql.*;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

// docker run -e "ACCEPT_EULA=Y" -e "SA_PASSWORD=<YourStrong@Passw0rd>" \
//   -p 1433:1433 --name sql1 --hostname sql1 \
//   -d mcr.microsoft.com/mssql/server:2019-latest

// The DatabaseConnection class is the utility that connects this java application to
// a SQL database and makes queries
// You will potentially need to update the server, port, database name, and database password depending
// on how you set up the database you're using. I'd suggest using a docker container which you can set up
// on a Mac or Linux machine by running the command above

// The queries used in this class are dependent on the names of the actual tables, which i've documented in the Readme
// in this repo, if you're having problems

public class DatabaseConnection {
    public static void main(String[] args) {
        Connection conn = null;
        // this is a little demo of some of the capabilities of the database connection
        try {
            System.out.println("trying connection");
            String server = "localhost";
            String port = "1433";
            String databaseName = "McGill_Billboard_Project";
            // the url is the address where the database is running
            // if it's running on your local machine then it'll be at localhost, otherwise you'll need a full url
            String url = "jdbc:sqlserver://" + server + ":" + port + ";DatabaseName=" + databaseName + ";encrypt=true;trustServerCertificate=true;";
            String username = "sa";
            String pass = "<YourStrong@Passw0rd>";
            // the connection object is the thing we're going to use to get and recieve data from the database
            conn = DriverManager.getConnection(url, username, pass);
            System.out.println("Successful connection!");
            System.out.println("Enter a chord: ");
            Scanner scan = new Scanner(System.in);
            String chord = scan.nextLine();
            List<String> songNames = querySongsByChordProgression(conn, chord);
            for (int i = 0; i < songNames.size(); i++) {
                System.out.println(songNames.get(i));
            }
        } catch (SQLException e) {
            throw new Error("Problem with SQL connection:", e);
        } finally {
            try {
                if (conn != null) {
                    // be sure to close the connection when we're done
                    conn.close();
                }
            } catch (SQLException ex) {
                System.out.println(ex.getMessage());
            }
        }
    }

    // A very simple function to get the first five rows of the song_summary table
    // not very useful except as a test that you've successfully connected to the database
    public static void viewSongSummary(Connection conn) throws SQLException {
        String query = "SELECT TOP (5) * FROM dbo.song_summary";
        try (Statement stmt = conn.createStatement()) {
            ResultSet rs = stmt.executeQuery(query);
            while (rs.next()) {
                int songID = rs.getInt("Song_ID");
                String songName = rs.getString("Song_Name");
                String artist = rs.getString("Artist");
                String metre = rs.getString("Metre").trim();
                String tonic = rs.getString("Tonic");
                String songSummaryRow = songID + ", " + songName + ", " + artist + ", " + metre + ", " + tonic;
                System.out.println(songSummaryRow);
            }
        } catch (SQLException e) {
            throw new Error("Problem with SQL Query:", e);
        }
    }

    // this returns every song by a particular artist in the database
    public static void querySongNameByArtist(Connection conn, String artist) throws SQLException {
        String query = "SELECT Song_Name FROM dbo.song_summary WHERE Artist = ?";
        try (Statement stmt = conn.createStatement()) {
            PreparedStatement preparedStatement = conn.prepareStatement(query);
            preparedStatement.setString(1, artist);
            ResultSet rs = preparedStatement.executeQuery();
            while (rs.next()) {
                String songName = rs.getString("Song_Name");
                System.out.println(songName);
            }
        }
    }

    // Returns the number of chords with a particular root note
    // Note: this currently writes directly to the terminal, you may want to adapt it to return an integer
    public static void queryNumChordsByRoot(Connection conn, String root) throws SQLException {
        String query = "SELECT Chord_Name FROM dbo.all_chords WHERE Chord_Name Like ?:%";
        try (Statement stmt = conn.createStatement()) {
            PreparedStatement preparedStatement = conn.prepareStatement(query);
            preparedStatement.setString(1, root);
            ResultSet rs = preparedStatement.executeQuery();
            int count = 0;
            while (rs.next()) {
                count ++;
            }
            System.out.println(count);
        }
    }

    // returns a list of the names of all songs which contains a particular chord
    // this method queries the regular chord notations of the type "C:maj"
    public static List<String> querySongsByChords(Connection conn, String chord) throws SQLException {
        String query = "SELECT song_summary.Song_Name FROM song_summary INNER JOIN UNIQUE_CHORDS_BY_SONG ON " +
                "song_summary.Song_ID = UNIQUE_CHORDS_BY_SONG.Song_ID WHERE UNIQUE_CHORDS_BY_SONG.Chords LIKE ?";
        List<String> listOfSongNames = new ArrayList<>();
        try {
            PreparedStatement preparedStatement = conn.prepareStatement(query);
            preparedStatement.setString(1, "%" + chord + "%");
            ResultSet rs = preparedStatement.executeQuery();
            while (rs.next()) {
                String songName = rs.getString("Song_Name");
                listOfSongNames.add(songName);
            }
        } catch (SQLException e) {
            throw new SQLException("Problem with SQL Query:", e);
        }
        if (listOfSongNames.isEmpty()) {
            throw new Error("No songs with chord: " + chord);
        }
        return listOfSongNames;
    }

    // returns a list of all the names of all the songs which contain a particular chord progression
    // this method queries the regular chord notations of the type "C:maj"
    public static List<String> querySongsByChordProgression(Connection conn, String chords) throws SQLException {
        String query = "SELECT song_summary.Song_Name FROM song_summary INNER JOIN songs_and_chords_no_repeats " +
                "ON song_summary.Song_ID = songs_and_chords_no_repeats.Song_ID WHERE songs_and_chords_no_repeats.Chords LIKE ?";
        List <String> listOfSongNames = new ArrayList<>();
        try {
            PreparedStatement preparedStatement = conn.prepareStatement(query);
            preparedStatement.setString(1, "%" + chords + "%");
            ResultSet rs = preparedStatement.executeQuery();
            while (rs.next()) {
                String songName = rs.getString("Song_Name");
                listOfSongNames.add(songName);
            }
        } catch (SQLException e) {
            throw new SQLException("Problem with SQL Query:", e);
        }
        if (listOfSongNames.isEmpty()) {
            throw new Error("No songs with the chord progression: " + chords);
        }
        return listOfSongNames;
    }

    // returns a list of all the names of all the songs which contain a particular chord progression
    // this method queries the roman chord notations of the type "I:maj"
    public static List<String> querySongsByRomanNumeralChordProgression(Connection conn, String chords) throws SQLException {
        String query = "SELECT song_summary.Song_Name FROM song_summary INNER JOIN roman_chords_no_repeats " +
                "ON song_summary.Song_ID = songs_and_chords_no_repeats.Song_ID WHERE songs_and_chords_no_repeats.Chords LIKE ?";
        List <String> listOfSongNames = new ArrayList<>();
        try {
            PreparedStatement preparedStatement = conn.prepareStatement(query);
            preparedStatement.setString(1, "%" + chords + "%");
            ResultSet rs = preparedStatement.executeQuery();
            while (rs.next()) {
                String songName = rs.getString("Song_Name");
                listOfSongNames.add(songName);
            }
        } catch (SQLException e) {
            throw new SQLException("Problem with SQL Query:", e);
        }
        if (listOfSongNames.isEmpty()) {
            throw new Error("No songs with the chord progression: " + chords);
        }
        return listOfSongNames;
    }
}
