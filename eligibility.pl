% eligibility.pl
:- use_module(library(csv)).
:- use_module(library(http/thread_httpd)).
:- use_module(library(http/http_dispatch)).
:- use_module(library(http/http_parameters)).
:- use_module(library(http/http_json)).
:- use_module(library(http/http_cors)).

% Dynamic predicates declaration
:- dynamic student/3.

% Load CSV data into Prolog
load_csv_data :-
    writeln('Loading CSV data...'),
    csv_read_file('students.csv', [_|Rows], []),  % Skip header row
    process_rows(Rows),
    writeln('CSV data loaded successfully.').

% Process CSV rows
process_rows([]).
process_rows([Row|Rest]) :-
    Row =.. [row,ID,Attendance,CGPA],
    % Convert only if the values are atoms
    (atom(Attendance) -> atom_number(Attendance, AttendanceNum)
                      ; AttendanceNum = Attendance),
    (atom(CGPA) -> atom_number(CGPA, CGPANum)
                 ; CGPANum = CGPA),
    assertz(student(ID,AttendanceNum,CGPANum)),
    process_rows(Rest).

% Rule to determine scholarship eligibility
eligible_for_scholarship(Student_ID) :-
    student(Student_ID, Attendance_percentage, CGPA),
    Attendance_percentage >= 75,
    CGPA >= 9.0.

% Rule to determine exam permission
permitted_for_exam(Student_ID) :-
    student(Student_ID, Attendance_percentage, _),
    Attendance_percentage >= 75.

% Define HTTP handlers
:- http_handler('/eligibility/scholarship', handle_scholarship, []).
:- http_handler('/eligibility/exam', handle_exam, []).

% Handler to check scholarship eligibility
handle_scholarship(Request) :-
    cors_enable,
    http_parameters(Request, [student_id(Student_ID, [])]),
    (eligible_for_scholarship(Student_ID) ->
        Reply = json{eligible: true}
    ;   Reply = json{eligible: false}
    ),
    reply_json(Reply).

% Handler to check exam permission
handle_exam(Request) :-
    cors_enable,
    http_parameters(Request, [student_id(Student_ID, [])]),
    (permitted_for_exam(Student_ID) ->
        Reply = json{permitted: true}
    ;   Reply = json{permitted: false}
    ),
    reply_json(Reply).

% Enable CORS
cors_enable :-
    format('Access-Control-Allow-Origin: *~n'),
    format('Access-Control-Allow-Methods: GET, POST, OPTIONS~n'),
    format('Access-Control-Allow-Headers: Content-Type~n').

% Start the server
server(Port) :-
    http_server(http_dispatch, [port(Port)]).

% Initialization
:- initialization((
    load_csv_data,
    server(8080)
)).