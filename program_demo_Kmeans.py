import pygame
from random import randint 
import math

from sklearn.cluster import KMeans
import numpy


pygame.init()

screen = pygame.display.set_mode((1000,500))
pygame.display.set_caption('KMeans Visualization')

# Create function draw text
def creat_text(string):
	font = pygame.font.SysFont('sans', 30)
	return font.render(string, True, SKY)

# Create function calculate distance
def distance(p,c):
	return math.sqrt((p[0]-c[0])*(p[0]-c[0]) + (p[1]-c[1])*(p[1]-c[1]))

BACKGROUND = (214, 214, 214)
BLACK = (0,0,0)
BACKGROUND_PANEL = (249, 255, 230)
WHITE = (255, 255, 255)

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (147, 153, 35)
PURPLE = (255, 0, 255)
SKY = (0, 255, 255)
ORANGE = (255, 125, 25)
GRAPE = (100, 25, 125)
GRASS = (55, 155, 65)

COLORS = [RED, GREEN, BLUE, YELLOW, PURPLE, SKY,ORANGE, GRAPE, GRASS]

# Creat text
text_plus = creat_text('+')
text_minus = creat_text('-')
text_run = creat_text('Run')
text_random = creat_text('Random')
text_algorithm = creat_text('Algorithm')
text_reset = creat_text('Reset')


clock = pygame.time.Clock()
running = True
K = 0
points = []
clusters = []
labels = []

while running:
	# Set frequen fps and background color
	clock.tick(60)
	screen.fill(BACKGROUND)
	# Get mouse position
	mouse_x, mouse_y = pygame.mouse.get_pos()

	# Draw interface
	pygame.draw.rect(screen, BLACK, (20,20,600,350))
	pygame.draw.rect(screen, BACKGROUND_PANEL, (22,22,596,346))

	# K button plus
	pygame.draw.rect(screen, BLACK, (700,20,30,30))
	screen.blit(text_plus, (708,15))

	# K button minus
	pygame.draw.rect(screen, BLACK, (760,20,30,30))
	screen.blit(text_minus, (770,15))

	# K Value, vi bien K thay doi gia tri nen can dua vao vong lap de khoi tao
	font = pygame.font.SysFont('sans', 30)
	text_k = font.render('K = ' + str(K), True, BLUE)
	screen.blit(text_k, (820,20))

	# Run button
	pygame.draw.rect(screen, BLACK, (700,90,120,30))
	screen.blit(text_run, (708,86))

	# Random button
	pygame.draw.rect(screen, BLACK, (700,150,120,30))
	screen.blit(text_random, (708,146))

	# Algorithm button
	pygame.draw.rect(screen, BLACK, (700,270,120,30))
	screen.blit(text_algorithm, (708,266))

	# Reset button
	pygame.draw.rect(screen, BLACK, (700,330,120,30))
	screen.blit(text_reset, (708,326))

	# End draw interface

	# Text mouse
	if 20<mouse_x<620 and 20<mouse_y<370:
		font = pygame.font.SysFont('sans', 15)
		text_mouse = font.render(f'({mouse_x-20},{mouse_y-20})', True, BLACK)
		screen.blit(text_mouse,(mouse_x+10,mouse_y))

	# Text Error
	Error = 0
	font = pygame.font.SysFont('sans', 30)
	if len(clusters) != 0 and len(labels) != 0:
		for i in range(len(points)):
			Error += distance(points[i], clusters[labels[i]])

	text_error = font.render(f'Error = {int(Error)}', True, BLACK)
	screen.blit(text_error, (708, 206))


	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		if event.type == pygame.MOUSEBUTTONDOWN:
			# Add points mouse
			if 20<mouse_x<620 and 20<mouse_y<370:
				point = [mouse_x-20, mouse_y-20]
				points.append(point)

			# Check mouse at K button plus
			if 700<mouse_x<730 and 20<mouse_y<50:
				K += 1
				if K > 8:
					K = 8
				print('K plus pressed')

			# Check mouse at K button minus
			if 760<mouse_x<790 and 20<mouse_y<50:
				K -= 1
				if K < 0:
					K = 0
				print('K minus pressed')

			# Check mouse at run button
			if 700<mouse_x<820 and 90<mouse_y<120:
				labels = []

				if len(clusters) == 0:
					continue

				for p in points:
					dis_points_to_cluster = []
					for c in clusters:
						dis = distance(p,c)
						dis_points_to_cluster.append(dis)

					dis_min = min(dis_points_to_cluster)
					labels.append(dis_points_to_cluster.index(dis_min))

				# Remove clusters
				for i in range(0, len(clusters)):
					sum_x = 0
					sum_y = 0
					count = 0
					for j in range(0, len(points)):
						if labels[j] == i:
							sum_x += points[j][0]
							sum_y += points[j][1]
							count += 1

					if count != 0:
						new_x_clusters = sum_x/count
						new_y_clusters = sum_y/count
						clusters[i] = [new_x_clusters, new_y_clusters]
				print('Run pressed')

			# Check mouse at random button
			if 700<mouse_x<820 and 150<mouse_y<180:
				labels = []
				clusters = []
				for i in range(K):
					random_point = [randint(0,600)+20, randint(0,350)+20]
					clusters.append(random_point)
				print('Random pressed')
				print(len(clusters))

			# Check mouse at algorithm button
			if 700<mouse_x<820 and 270<mouse_y<300:
				if K == 0 or len(points) == 0:
					continue

				kmeans = KMeans(n_clusters = K).fit(points)
				clusters = kmeans.cluster_centers_
				labels = kmeans.predict(points)
				print('Algorithm pressed')

			# Check mouse at reset button
			if 700<mouse_x<820 and 330<mouse_y<360:
				K = 0
				points = []
				clusters = []
				labels = []
				Error = 0
				print('Reset pressed')

	# Draw cluster point
	for j in range(len(clusters)):
		pygame.draw.circle(screen, COLORS[j], (clusters[j][0], clusters[j][1]), 6)


	# Draw points
	for i in range(len(points)):
		pygame.draw.circle(screen, BLACK, (points[i][0]+20, points[i][1]+20), 4)
		if len(labels) == 0:
			pygame.draw.circle(screen, WHITE, (points[i][0]+20, points[i][1]+20), 3.5)
		else:
			pygame.draw.circle(screen, COLORS[labels[i]], (points[i][0]+20, points[i][1]+20), 3.5)




	pygame.display.flip()

pygame.quit()
