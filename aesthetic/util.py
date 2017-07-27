def normalize(x, expected_min, expected_max):
  size = expected_max - expected_min
  result = max(min((x - expected_min) / size, 1.0), 0.0)
  return result

