
# Confirmers
AuthorityID_table = dict()
AuthorityID_table['1'] = "משרד החקלאות"
AuthorityID_table['2'] = "משרד התחבורה"
AuthorityID_table['3'] = "משרד הכלכלה"
AuthorityID_table['4'] = "מכון התקנים"
AuthorityID_table['5'] = "רשות המיסים"
AuthorityID_table['6'] = "המשרד להגנת הסביבה"
AuthorityID_table['7'] = "משרד הבריאות"
AuthorityID_table['8'] = "משרד הבטחון"
AuthorityID_table['9'] = "משרד ראש הממשלה"
AuthorityID_table['10'] = "משרד האנרגיה"
AuthorityID_table['11'] = "הרבנות הראשית"
AuthorityID_table['12'] = "המשרד לבטחון פנים"
AuthorityID_table['13'] = "משרד התקשורת"
AuthorityID_table['15'] = "משרד התרבות והספורט"
AuthorityID_table['16'] = "משרד החינוך"
AuthorityID_table['18'] = "משרד הבינוי והשיכון"
AuthorityID_table['19'] = "נציגות קונסולרית ישראלית בחוץ לארץ"
AuthorityID_table['21'] = "רשות העתיקות"
AuthorityID_table['23'] = "המנהל האזרחי"
AuthorityID_table['24'] = "מעבדת בדיקה"

Regulations = {
    '0101':  'אישור השירות הוטרינרי', '0102':  'אישור הגנת הצומח', '0103':  'אישור טיב מספוא', '0104':  'אישור מיכון וטכנולוגיה',
    '0105':  'אישור אגף הדייג', '0107':  'אישור המנכ"ל', '0109':  'רשיון המרכז לסחר חוץ', '0110':  'רשיון הרשות לתכנון חקלאות וכלכלה',
    '0201':  'אישור אגף הרכב ושרותי תחזוקה', '0202':  'רשיון אגף הרכב ושירותי תחזוקה - גף צמ"ה', '0203':  'רשיון אגף הרכבות', '0204':  'מעבדה מוסמכת לרכב',
    '0209':  'הועדה הבין משרדית להתקני תנועה ובטיחות', '0210':  'רשיון אגף הרכב ושרותי תחזוקה',
    '0212':  'רישיון לסחר במוצרי תעבורה', '0213':  'רישיון לסחר במערכות גפ"מ לרכב', '0214':  'רישיון לסחר בצמיגים',
    '0215':  'רשיון אוטונומיה', '0217':  'רישיון אגף הרכב ושרותי תחזוקה - יבוא אישי', '0218':  'אישור אגף הרכב ושרותי תחזוקה - יבוא אישי',
    '0219':  'אישור אגף הרכב ושירותי תחזוקה - גף צמ"ה', '0221':  'רשיון רשות התעופה האזרחית', '0222':  'רשיון רשות הספנות והנמלים',
    '0302':  'אישור מידות ומשקלות', '0303':  'אישור מנכ"ל', '0305':  'אישור כלכלה', '0307':  'אישור מפקח על היהלומים',
    '0308':  'רישיון מינהל תעשיות', '0309':  'רישיון צי"ח מנהל היהלומים', '0310':  'מינהל היבוא - רישיון צי"ח מחוז המרכז',
    '0311':  'רישיון מינהל סביבה ופיתוח בר קיימא', '0315':  'רשיון צי"ח 6(3) ארצות אסורות',
    '0319':  'אישור התרת ציוד דו-שימושי לתחומי הרש"פ', '0325':  'אישור שחרור',
    '0402':  'אישור לשחרור',
    '0501':  'אישור מנהל',
    '0602':  'אישור חומרים מסוכנים', '0603':  'אישור ממונה על הקרינה', '0604':  'ת.רשום ע"פ תקנות תכשרים להדברה',
    '0701':  'אישור שירות המזון', '0702':  'אישור אגף הרוקחות', '0703':  'אישור אמ"ר', '0704':  'רשיון אגף הרוקחות',
    '0705':  'אישור שחרור תחנת מעבר', '0706':  'אגף הרוקחות - רשיון ע"פ צו התמרוקים', '0708':  'אישור מכשירי קרינה',
    '0709':  'אישור מנכ"ל בריאות', '0710':  'אישור אגף הרוקחות - סמים', '0713':  'אישור 2ג2 - אגף הרוקחות',
    '0715':  'רשיון לתכשיר לפי צו תכשירים להדברת מזיקים לאדם',
    '0804':  'רשיון ליבוא אמל"ח',
    '1001':  'אישור אגף ניהול משאבי תשתיות',
    '1101':  'תעודת הכשר',
    '1201':  'אישור ביטחון פנים', '1203':  'רשיון אגף לפיקוח ורשוי כלי ירייה', '1204':  'אישור מפקח על הכבאות',
    '1301':  'אישור תקשורת',
    '2101':  'אישור רשות העתיקות',
    '2301':  'אישור קמ"ט תקשורת', '2303':  'אישור קמ"ט הגנת הסביבה',
    '2402':  'אישור שחרור מותנה',
    'אישור אגף ניהול משאבי תשתיות':  '', 'אישור יצוא שירותים להגנת הצומח':  '', 'אישור מפמכ':  '', 'רשיון יבוא':  '',
    'רשיון יבוא מלשכת הבריאות בנפת רמלה':  '', 'רשיון יצוא אגף הרכב ושירותי תחזוקה ': ''

}


def regulation_from_code(code):
    if code in Regulations.keys():
        if Regulations[code] is None or Regulations[code] == '':
            return code
        else:
            return Regulations[code]
    else:
        return code


def confirmer_from_code(code_val):
    code = str(code_val)
    if code in AuthorityID_table.keys():
        if AuthorityID_table[code] is None or AuthorityID_table[code] == '':
            return code
        else:
            return AuthorityID_table[code]
    else:
        return code
