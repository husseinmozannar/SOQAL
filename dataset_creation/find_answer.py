def editDistance(str1, str2, m, n):
    # edit distance recursive implementation, m = len(str1) and n = len(str2)
    dp = [[0 for x in range(n + 1)] for x in range(m + 1)]
    for i in range(m + 1):
        for j in range(n + 1):
            if i == 0:
                dp[i][j] = j  # Min. operations = j

            elif j == 0:
                dp[i][j] = i  # Min. operations = i
            elif str1[i - 1] == str2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i][j - 1],  # Insert
                                   dp[i - 1][j],  # Remove
                                   dp[i - 1][j - 1])  # Replace

    return dp[m][n]


def concatenateString(paragraph, start, length):
    final_string = paragraph[start]
    for i in range(1, length):
        final_string += " " + paragraph[start + i]
    return final_string

def find_answer(paragraph, answer):
    # check if answer already in paragraph
    correct_answer = ""
    score_answer = 1000000
    para_words = paragraph.split()
    for i in range(0, len(para_words)):
        # check max 15 word ranges, reduced for efficiency
        for j in range(1, min(15, len(para_words) - i+1)):
            candidate = concatenateString(para_words, i, j)
            if candidate == answer:
                return answer, paragraph.find(answer)
            score = editDistance(answer, candidate, len(answer), len(candidate))
            if (score < score_answer):
                score_answer = score
                correct_answer = candidate
    return correct_answer, paragraph.find(correct_answer)

def test_find_answer():
    p = "أصبحت بلاكبول وبلاكبيرن مع داروين سلطات وحدوية مستقلة "
    a = "بلاكبو"
    print(find_answer(p, a))
