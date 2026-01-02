-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jan 02, 2026 at 05:18 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `whiteschollars`
--

-- --------------------------------------------------------

--
-- Table structure for table `accreditationsandcertification`
--

CREATE TABLE `accreditationsandcertification` (
  `id` bigint(20) NOT NULL,
  `certification_logo` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`certification_logo`)),
  `course_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `accreditationsandcertification`
--

INSERT INTO `accreditationsandcertification` (`id`, `certification_logo`, `course_id`) VALUES
(7, '[\"/media/accreditations_certifications/future-skill.svg\", \"/media/accreditations_certifications/linkedin.svg\", \"/media/accreditations_certifications/meta.webp\", \"/media/accreditations_certifications/microsoft.svg\"]', 1),
(8, '[\"/media/accreditations_certifications/download_WNF03GA.png\", \"/media/accreditations_certifications/download_2sgmM0M.png\", \"/media/accreditations_certifications/download_TUVnxXs.png\"]', 2);

-- --------------------------------------------------------

--
-- Table structure for table `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL,
  `name` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_group_permissions`
--

CREATE TABLE `auth_group_permissions` (
  `id` bigint(20) NOT NULL,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_permission`
--

CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add log entry', 1, 'add_logentry'),
(2, 'Can change log entry', 1, 'change_logentry'),
(3, 'Can delete log entry', 1, 'delete_logentry'),
(4, 'Can view log entry', 1, 'view_logentry'),
(5, 'Can add permission', 2, 'add_permission'),
(6, 'Can change permission', 2, 'change_permission'),
(7, 'Can delete permission', 2, 'delete_permission'),
(8, 'Can view permission', 2, 'view_permission'),
(9, 'Can add group', 3, 'add_group'),
(10, 'Can change group', 3, 'change_group'),
(11, 'Can delete group', 3, 'delete_group'),
(12, 'Can view group', 3, 'view_group'),
(13, 'Can add user', 4, 'add_user'),
(14, 'Can change user', 4, 'change_user'),
(15, 'Can delete user', 4, 'delete_user'),
(16, 'Can view user', 4, 'view_user'),
(17, 'Can add content type', 5, 'add_contenttype'),
(18, 'Can change content type', 5, 'change_contenttype'),
(19, 'Can delete content type', 5, 'delete_contenttype'),
(20, 'Can view content type', 5, 'view_contenttype'),
(21, 'Can add session', 6, 'add_session'),
(22, 'Can change session', 6, 'change_session'),
(23, 'Can delete session', 6, 'delete_session'),
(24, 'Can view session', 6, 'view_session'),
(25, 'Can add course', 7, 'add_course'),
(26, 'Can change course', 7, 'change_course'),
(27, 'Can delete course', 7, 'delete_course'),
(28, 'Can view course', 7, 'view_course'),
(29, 'Can add section', 8, 'add_section'),
(30, 'Can change section', 8, 'change_section'),
(31, 'Can delete section', 8, 'delete_section'),
(32, 'Can view section', 8, 'view_section'),
(33, 'Can add key highlight', 9, 'add_keyhighlight'),
(34, 'Can change key highlight', 9, 'change_keyhighlight'),
(35, 'Can delete key highlight', 9, 'delete_keyhighlight'),
(36, 'Can view key highlight', 9, 'view_keyhighlight'),
(37, 'Can add accreditations and certification', 10, 'add_accreditationsandcertification'),
(38, 'Can change accreditations and certification', 10, 'change_accreditationsandcertification'),
(39, 'Can delete accreditations and certification', 10, 'delete_accreditationsandcertification'),
(40, 'Can view accreditations and certification', 10, 'view_accreditationsandcertification'),
(41, 'Can add why choose', 11, 'add_whychoose'),
(42, 'Can change why choose', 11, 'change_whychoose'),
(43, 'Can delete why choose', 11, 'delete_whychoose'),
(44, 'Can view why choose', 11, 'view_whychoose'),
(45, 'Can add mentor', 12, 'add_mentor'),
(46, 'Can change mentor', 12, 'change_mentor'),
(47, 'Can delete mentor', 12, 'delete_mentor'),
(48, 'Can view mentor', 12, 'view_mentor'),
(49, 'Can add program highlight', 13, 'add_programhighlight'),
(50, 'Can change program highlight', 13, 'change_programhighlight'),
(51, 'Can delete program highlight', 13, 'delete_programhighlight'),
(52, 'Can view program highlight', 13, 'view_programhighlight'),
(53, 'Can add career assistance', 14, 'add_careerassistance'),
(54, 'Can change career assistance', 14, 'change_careerassistance'),
(55, 'Can delete career assistance', 14, 'delete_careerassistance'),
(56, 'Can view career assistance', 14, 'view_careerassistance'),
(57, 'Can add career transition', 15, 'add_careertransition'),
(58, 'Can change career transition', 15, 'change_careertransition'),
(59, 'Can delete career transition', 15, 'delete_careertransition'),
(60, 'Can view career transition', 15, 'view_careertransition'),
(61, 'Can add our alumni', 16, 'add_ouralumni'),
(62, 'Can change our alumni', 16, 'change_ouralumni'),
(63, 'Can delete our alumni', 16, 'delete_ouralumni'),
(64, 'Can view our alumni', 16, 'view_ouralumni'),
(65, 'Can add on campus class', 17, 'add_oncampusclass'),
(66, 'Can change on campus class', 17, 'change_oncampusclass'),
(67, 'Can delete on campus class', 17, 'delete_oncampusclass'),
(68, 'Can view on campus class', 17, 'view_oncampusclass'),
(69, 'Can add fee structure', 18, 'add_feestructure'),
(70, 'Can change fee structure', 18, 'change_feestructure'),
(71, 'Can delete fee structure', 18, 'delete_feestructure'),
(72, 'Can view fee structure', 18, 'view_feestructure'),
(73, 'Can add program for', 19, 'add_programfor'),
(74, 'Can change program for', 19, 'change_programfor'),
(75, 'Can delete program for', 19, 'delete_programfor'),
(76, 'Can view program for', 19, 'view_programfor'),
(77, 'Can add why white scholars', 20, 'add_whywhitescholars'),
(78, 'Can change why white scholars', 20, 'change_whywhitescholars'),
(79, 'Can delete why white scholars', 20, 'delete_whywhitescholars'),
(80, 'Can view why white scholars', 20, 'view_whywhitescholars'),
(81, 'Can add listen our expert', 21, 'add_listenourexpert'),
(82, 'Can change listen our expert', 21, 'change_listenourexpert'),
(83, 'Can delete listen our expert', 21, 'delete_listenourexpert'),
(84, 'Can view listen our expert', 21, 'view_listenourexpert');

-- --------------------------------------------------------

--
-- Table structure for table `auth_user`
--

CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `auth_user`
--

INSERT INTO `auth_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`) VALUES
(1, 'pbkdf2_sha256$600000$CbNxiJeTobI9nJo3mKtw0r$ekPxPm8fWk6O8VmqZ7UspAL9LHV+5yQA1EH3KHFkwbo=', '2025-11-12 02:54:48.216170', 1, 'admin', '', '', 'admin@gmail.com', 1, 1, '2025-11-08 13:24:04.560562');

-- --------------------------------------------------------

--
-- Table structure for table `auth_user_groups`
--

CREATE TABLE `auth_user_groups` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_user_user_permissions`
--

CREATE TABLE `auth_user_user_permissions` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `career_assistance`
--

CREATE TABLE `career_assistance` (
  `id` bigint(20) NOT NULL,
  `title` varchar(255) NOT NULL,
  `description` longtext NOT NULL,
  `description_list` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`description_list`)),
  `image` varchar(100) DEFAULT NULL,
  `course_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `career_assistance`
--

INSERT INTO `career_assistance` (`id`, `title`, `description`, `description_list`, `image`, `course_id`) VALUES
(2, 'Placement Methodology ssr', 'At Whitescholars, our placement methodology is designed to ensure that every student is industry ready and confident to face the real world challenges. Students are made to understand the specific hiring requirements of the companies and trained with our crashed courses as per the job description.', '[\"Interactive group discussions and Jam sessions\", \"Student activities to develop interpersonal skills\", \"Develop essential soft skills to effective present yourself.\"]', 'career_assistance/test_v8wT6Y1.jpg', 1),
(3, 'Resume Optimization and Portfolio Building', 'Get resume tips and upgrade it to make it more professional and impressive, so it stands out to recruiters correctly. Get guidance to build a strong portfolio that shows skills, real-time projects, and achievements in a professional way. Learn how to highlight strengths and tailor resumes for different roles. Structure your portfolio to reflect technical expertise and problem-solving abilities. Present your journey, growth, and real-time experience with confidence and clarity. Stand out to recruiters with a powerful resume and portfolio that showcase skills, projects, and potential.', '[\"20+ sample resumes.\", \"Github profile building.\", \"Project portfolio creation.\", \"Get tips to make ATS friendly resume.\", \"Exclusive resume guidance classes by the placement coordinator.\", \"Customised Resume as per the Job description and company profile.\", \"One-on-one resume Feedback and Suggestion tips to avoid common resume mistakes.\"]', 'career_assistance/test_dCHX3nA.jpg', 1),
(4, 'LinkedIn Optimization', 'Get help to optimize your LinkedIn profile and make it look more professional and impressive to grab recruiters attention, boosting visibility, helping more people to connect, and growing professional network. WhiteScholars guides on how to write a strong headline, craft a clear summary, and highlight your skills, projects, and achievements in the right way. An optimized linkedin profile can open doors for your career. Make your LinkedIn profile work for you and get noticed by the right people.', '[\"Get tips to optimize Linkedin.\", \"Learn how to build more connection and professional network with HRs.\", \"Explore and understand the best practices for writing impactful LinkedIn headlines and summaries that catch the recruiter\'s attention.\", \"Learn certificate and project updation in the featured section.\", \"Learn how to find company HR\\u2019s contact information.\"]', 'career_assistance/test_zK4chqU.jpg', 1),
(5, 'Interview Preparation Support', 'Get interview tips and get prepared with mock interview sessions that help you boost confidence. Receive personalized feedback to improve your performance. Our expert mentors create real-time interview scenarios, helping to get comfortable with both technical and HR rounds. Learn how to handle difficult questions, structure your responses, and make a strong first impression. Our goal is to help you not just crack the interview but stand out.', '[\"Interactive group discussions and Jam sessions\", \"Student activities to develop interpersonal skills\", \"Develop essential soft skills to effective present yourself.\", \"Regular project presentations to improve presentation skills.\", \"Build strong leadership skills and the potential to work effectively in teams.\", \"Improve your decision-making abilities through practical and real-world case studies.\"]', 'career_assistance/test_T3wZXn6.jpg', 1);

-- --------------------------------------------------------

--
-- Table structure for table `career_transitions`
--

CREATE TABLE `career_transitions` (
  `id` bigint(20) NOT NULL,
  `name` varchar(255) NOT NULL,
  `designation` varchar(255) NOT NULL,
  `description` longtext NOT NULL,
  `placed_company` varchar(255) NOT NULL,
  `job_type` varchar(255) NOT NULL,
  `youtube_testimonial_link` varchar(500) DEFAULT NULL,
  `course_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `career_transitions`
--

INSERT INTO `career_transitions` (`id`, `name`, `designation`, `description`, `placed_company`, `job_type`, `youtube_testimonial_link`, `course_id`) VALUES
(2, 'Meghna Velluri', 'Junior Data Scientist', 'Whitescholars have helped in gaining industry knowledge with this Data Science course. I am thankful to every mentor for supporting me and giving me the right opportunity.', 'UST', 'Fresher', 'https://www.youtube.com/embed/GBmmQyNW_6o', 1),
(3, 'Meghna Velluri', 'Junior Data Scientist', 'Whitescholars have helped in gaining industry knowledge with this Data Science course. I am thankful to every mentor for supporting me and giving me the right opportunity.', 'UST', 'Fresher', 'https://www.youtube.com/embed/GBmmQyNW_6o', 1),
(4, 'Meghna Velluri', 'Junior Data Scientist', 'Whitescholars have helped in gaining industry knowledge with this Data Science course. I am thankful to every mentor for supporting me and giving me the right opportunity.', 'UST', 'Fresher', 'https://www.youtube.com/embed/GBmmQyNW_6o', 1),
(5, 'Meghna Velluri', 'Junior Data Scientist', 'Whitescholars have helped in gaining industry knowledge with this Data Science course. I am thankful to every mentor for supporting me and giving me the right opportunity.', 'UST', 'Fresher', 'https://www.youtube.com/embed/GBmmQyNW_6o', 1);

-- --------------------------------------------------------

--
-- Table structure for table `courses`
--

CREATE TABLE `courses` (
  `id` bigint(20) NOT NULL,
  `name` varchar(255) NOT NULL,
  `slug` varchar(50) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `meta_description` longtext DEFAULT NULL,
  `meta_keywords` varchar(500) DEFAULT NULL,
  `meta_og_image` varchar(100) DEFAULT NULL,
  `meta_title` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `courses`
--

INSERT INTO `courses` (`id`, `name`, `slug`, `created_at`, `meta_description`, `meta_keywords`, `meta_og_image`, `meta_title`) VALUES
(1, 'Data Science', 'data-science', '2025-11-04 17:55:11.947190', 'sdfsdfsdfsdfsdfsdf', 'sfsdfsdfsdfsdf', 'seo_images/download_rbWuafg.webp', 'sdfsdfsd'),
(2, 'digital marketing', 'digital-marketing', '2025-11-04 17:55:43.937393', NULL, NULL, NULL, NULL),
(3, 'Data Analytics', 'advanced-data-science-certification-course-in-hyde', '2025-11-12 02:57:13.712663', NULL, NULL, NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `course_intro`
--

CREATE TABLE `course_intro` (
  `id` bigint(20) NOT NULL,
  `logo` varchar(100) DEFAULT NULL,
  `section_heading` varchar(255) NOT NULL,
  `text` longtext DEFAULT NULL,
  `list_text` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`list_text`)),
  `collaboration_logo` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`collaboration_logo`)),
  `youtube_video` varchar(200) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `course_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `course_intro`
--

INSERT INTO `course_intro` (`id`, `logo`, `section_heading`, `text`, `list_text`, `collaboration_logo`, `youtube_video`, `created_at`, `course_id`) VALUES
(12, 'logos/50a37a7e-879a-4aaa-ac5f-3f75f18813c7.png.webp', 'Data Science & Gen AI Certification Course In Hyderabad check icon  Job - Ready Course', 'Launch your career as a Data Scientist with in-demand skills like Machine Learning, Gen AI, Tableau, and SQL. Our Data Science and Gen AI Course in Hyderabad is designed to make you industry-ready with real-world projects.', '[\"Mode: Offline | Online | Live Recorded Sessions\", \"180 Hours of learning\", \"Guaranteed virtual internships with Accenture & PWC\", \"Certificates from Nasscom and Microsoft\", \"7+ Real Time projects & 1 individual projects\", \"Guaranteed Interview Opportunities\"]', '[\"microsoft.svg\", \"pwc.png\", \"nasscom.svg\", \"accenture.svg\"]', 'https://youtu.be/FkSnZIyNoTQ', '2025-11-09 11:03:12.045703', 1);

-- --------------------------------------------------------

--
-- Table structure for table `django_admin_log`
--

CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) UNSIGNED NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `django_content_type`
--

CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(1, 'admin', 'logentry'),
(3, 'auth', 'group'),
(2, 'auth', 'permission'),
(4, 'auth', 'user'),
(5, 'contenttypes', 'contenttype'),
(10, 'dashboard', 'accreditationsandcertification'),
(14, 'dashboard', 'careerassistance'),
(15, 'dashboard', 'careertransition'),
(7, 'dashboard', 'course'),
(18, 'dashboard', 'feestructure'),
(9, 'dashboard', 'keyhighlight'),
(21, 'dashboard', 'listenourexpert'),
(12, 'dashboard', 'mentor'),
(17, 'dashboard', 'oncampusclass'),
(16, 'dashboard', 'ouralumni'),
(19, 'dashboard', 'programfor'),
(13, 'dashboard', 'programhighlight'),
(8, 'dashboard', 'section'),
(11, 'dashboard', 'whychoose'),
(20, 'dashboard', 'whywhitescholars'),
(6, 'sessions', 'session');

-- --------------------------------------------------------

--
-- Table structure for table `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2025-11-04 17:02:54.301284'),
(2, 'auth', '0001_initial', '2025-11-04 17:02:55.544634'),
(3, 'admin', '0001_initial', '2025-11-04 17:02:55.834884'),
(4, 'admin', '0002_logentry_remove_auto_add', '2025-11-04 17:02:55.848932'),
(5, 'admin', '0003_logentry_add_action_flag_choices', '2025-11-04 17:02:55.859836'),
(6, 'contenttypes', '0002_remove_content_type_name', '2025-11-04 17:02:56.063709'),
(7, 'auth', '0002_alter_permission_name_max_length', '2025-11-04 17:02:56.206160'),
(8, 'auth', '0003_alter_user_email_max_length', '2025-11-04 17:02:56.234211'),
(9, 'auth', '0004_alter_user_username_opts', '2025-11-04 17:02:56.248690'),
(10, 'auth', '0005_alter_user_last_login_null', '2025-11-04 17:02:56.352802'),
(11, 'auth', '0006_require_contenttypes_0002', '2025-11-04 17:02:56.360587'),
(12, 'auth', '0007_alter_validators_add_error_messages', '2025-11-04 17:02:56.384925'),
(13, 'auth', '0008_alter_user_username_max_length', '2025-11-04 17:02:56.414584'),
(14, 'auth', '0009_alter_user_last_name_max_length', '2025-11-04 17:02:56.438988'),
(15, 'auth', '0010_alter_group_name_max_length', '2025-11-04 17:02:56.466384'),
(16, 'auth', '0011_update_proxy_permissions', '2025-11-04 17:02:56.482569'),
(17, 'auth', '0012_alter_user_first_name_max_length', '2025-11-04 17:02:56.514017'),
(18, 'sessions', '0001_initial', '2025-11-04 17:02:56.581654'),
(19, 'dashboard', '0001_initial', '2025-11-04 17:04:54.860007'),
(21, 'dashboard', '0002_accreditationsandcertification', '2025-11-05 18:37:37.181829'),
(22, 'dashboard', '0003_whychoose', '2025-11-06 15:50:34.899226'),
(23, 'dashboard', '0004_mentor', '2025-11-06 16:12:49.011416'),
(24, 'dashboard', '0005_programhighlight', '2025-11-06 16:40:57.983461'),
(25, 'dashboard', '0006_careerassistance', '2025-11-06 18:04:44.058645'),
(26, 'dashboard', '0007_careertransition', '2025-11-06 18:17:14.008342'),
(27, 'dashboard', '0008_ouralumni', '2025-11-06 19:13:34.583919'),
(28, 'dashboard', '0009_oncampusclass', '2025-11-06 19:48:54.605207'),
(29, 'dashboard', '0010_alter_oncampusclass_time', '2025-11-06 19:51:24.003705'),
(30, 'dashboard', '0011_feestructure', '2025-11-08 09:14:05.581123'),
(31, 'dashboard', '0012_programfor', '2025-11-08 10:10:41.237222'),
(32, 'dashboard', '0013_whywhitescholars', '2025-11-08 10:27:28.092845'),
(33, 'dashboard', '0014_listenourexpert', '2025-11-08 11:15:50.072724'),
(34, 'dashboard', '0015_alter_listenourexpert_course', '2025-11-08 11:20:01.976975'),
(35, 'dashboard', '0016_oncampusclass_class_title', '2025-11-13 17:11:56.096825'),
(36, 'dashboard', '0017_course_meta_description_course_meta_keywords_and_more', '2025-11-15 08:41:38.153497'),
(37, 'dashboard', '0018_remove_course_description', '2025-11-15 08:47:54.236452');

-- --------------------------------------------------------

--
-- Table structure for table `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('eytq483ogk5amfmphmflnfr658whpqnx', '.eJxVjDsOwjAQBe_iGlnZxB9MSZ8zRLveNQ4gW4qTCnF3iJQC2jcz76Um3NY8bU2WaWZ1UaBOvxthfEjZAd-x3KqOtazLTHpX9EGbHivL83q4fwcZW_7WEc9kOopsexowJe8MWEogAaIHsowQjJHkxAdBb_qBUaztHDhBEafeHwfWOLw:1vJ10S:-jS_eu2iEXeV_DdZnwrFWNNzXpwishuQw1JLPqQtvig', '2025-11-26 02:54:48.222301');

-- --------------------------------------------------------

--
-- Table structure for table `fee_structures`
--

CREATE TABLE `fee_structures` (
  `id` bigint(20) NOT NULL,
  `title` varchar(255) NOT NULL,
  `mode_of_training` varchar(255) NOT NULL,
  `list_text` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`list_text`)),
  `batch_date` varchar(255) NOT NULL,
  `original_price` decimal(10,2) NOT NULL,
  `discount_price` decimal(10,2) NOT NULL,
  `course_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `fee_structures`
--

INSERT INTO `fee_structures` (`id`, `title`, `mode_of_training`, `list_text`, `batch_date`, `original_price`, `discount_price`, `course_id`) VALUES
(2, 'Instructor Led Training', 'Online', '[\"Online classes: weekdays\", \"Access to online class recordings for 365 days\", \"No cost EMI facility\", \"Informative sessions from Industry Experts\", \"Project presentations to guest faculties\", \"Interview support services\", \"Guranteed Interview opportunities\"]', '2025-11-18', 89999.00, 69999.00, 1),
(3, 'Physical Classroom Session', 'Classroom', '[\"Only 20 students in one classroom\", \"No cost EMI facility\", \"Lifetime access to live recorded sessions\", \"Informative sessions from Industry experts\", \"Project presentations to guest faculties\", \"360 degree career assistance\", \"Guranteed Interview opportunities\"]', '2025-11-20', 94999.00, 74999.00, 1);

-- --------------------------------------------------------

--
-- Table structure for table `key_highlight`
--

CREATE TABLE `key_highlight` (
  `id` bigint(20) NOT NULL,
  `logo` varchar(100) DEFAULT NULL,
  `text` longtext DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `course_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `key_highlight`
--

INSERT INTO `key_highlight` (`id`, `logo`, `text`, `created_at`, `course_id`) VALUES
(1, 'key_highlights/download_rbWuafg.png', 'Hybrid Mode of learning (Online, Offline and access to live recorded sessions)\n\n', '2025-11-05 17:00:36.895465', 1),
(2, 'key_highlights/download_QxJ7JL0.png', 'Hybrid Mode of learning (Online, Offline and access to live recorded sessions)', '2025-11-05 19:10:40.128130', 1);

-- --------------------------------------------------------

--
-- Table structure for table `listen_our_expert`
--

CREATE TABLE `listen_our_expert` (
  `id` bigint(20) NOT NULL,
  `title` varchar(255) NOT NULL,
  `youtube_links` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`youtube_links`)),
  `course_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `listen_our_expert`
--

INSERT INTO `listen_our_expert` (`id`, `title`, `youtube_links`, `course_id`) VALUES
(2, '“Listen to expert on why projects are important to crack interview for Data Science roles”', '[\"https://youtu.be/GBmmQyNW_6o\", \"https://youtu.be/GBmmQyNW_6o\", \"https://youtu.be/GBmmQyNW_6o\"]', 1);

-- --------------------------------------------------------

--
-- Table structure for table `mentors`
--

CREATE TABLE `mentors` (
  `id` bigint(20) NOT NULL,
  `mentor_image` varchar(100) DEFAULT NULL,
  `mentor_name` varchar(255) NOT NULL,
  `designation_name` varchar(255) NOT NULL,
  `experience_text` longtext NOT NULL,
  `company_logo` varchar(100) DEFAULT NULL,
  `course_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `mentors`
--

INSERT INTO `mentors` (`id`, `mentor_image`, `mentor_name`, `designation_name`, `experience_text`, `company_logo`, `course_id`) VALUES
(3, 'mentors/img-1.webp', 'Swapnil ssr', 'Sr. Data Analyst', '20 Years Experience', 'mentor_company_logos/logo-1.webp', 1),
(4, 'mentors/img-2.webp', 'Vishnu Murthy', 'Sr. Data Scientist', '20 Years Experience', 'mentor_company_logos/logo-2.webp', 1),
(5, 'mentors/img-3.webp', 'Satya Kumar', 'Sr. Data Scientist', '20 Years Experience', 'mentor_company_logos/logo-3.webp', 1),
(6, 'mentors/img-4.webp', 'Satish', 'Sr. Data Scientist', '20 Years Experience', 'mentor_company_logos/logo-4.webp', 1);

-- --------------------------------------------------------

--
-- Table structure for table `on_campus_classes`
--

CREATE TABLE `on_campus_classes` (
  `id` bigint(20) NOT NULL,
  `date` date NOT NULL,
  `time` varchar(100) NOT NULL,
  `batch_type` varchar(100) NOT NULL,
  `course_id` bigint(20) NOT NULL,
  `class_title` varchar(200) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `on_campus_classes`
--

INSERT INTO `on_campus_classes` (`id`, `date`, `time`, `batch_type`, `course_id`, `class_title`) VALUES
(1, '2025-11-28', '11:00 AM – 1:00 PM IST', 'Weekdays & Weekend', 1, 'Program Induction');

-- --------------------------------------------------------

--
-- Table structure for table `our_alumni`
--

CREATE TABLE `our_alumni` (
  `id` bigint(20) NOT NULL,
  `alumni_logo` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`alumni_logo`)),
  `course_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `our_alumni`
--

INSERT INTO `our_alumni` (`id`, `alumni_logo`, `course_id`) VALUES
(3, '[\"alumni_logos/download_rbWuafg.webp\", \"alumni_logos/download_rbWuafg.webp\", \"alumni_logos/download_rbWuafg.webp\", \"alumni_logos/download_rbWuafg.webp\", \"alumni_logos/download_rbWuafg.webp\"]', 1);

-- --------------------------------------------------------

--
-- Table structure for table `program_for`
--

CREATE TABLE `program_for` (
  `id` bigint(20) NOT NULL,
  `image` varchar(100) DEFAULT NULL,
  `title` varchar(255) NOT NULL,
  `description` longtext NOT NULL,
  `course_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `program_for`
--

INSERT INTO `program_for` (`id`, `image`, `title`, `description`, `course_id`) VALUES
(2, 'program_for_images/GROUPOFPEOPLE-300x200.jpg.webp', 'Freshers/Begginers', 'Just starting your career? Our data science course in Hyderabad is perfect for graduates from any field who want to step into data science and AI. No coding experience required.\r\n', 1),
(3, 'program_for_images/GROUPOFPEOPLE-300x200.jpg_IiMevrZ.webp', 'Data Enthusiasts', 'If you love working with numbers, spotting patterns, and making decisions based on data, this data scientist training in Hyderabad will help you sharpen your skills and take them to the next level.', 1);

-- --------------------------------------------------------

--
-- Table structure for table `program_highlights`
--

CREATE TABLE `program_highlights` (
  `id` bigint(20) NOT NULL,
  `title` varchar(255) NOT NULL,
  `heading` varchar(255) NOT NULL,
  `text` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`text`)),
  `image` varchar(100) DEFAULT NULL,
  `course_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `program_highlights`
--

INSERT INTO `program_highlights` (`id`, `title`, `heading`, `text`, `image`, `course_id`) VALUES
(4, 'Data Scientists as Trainers ssr', 'Master data science from experts who make concepts fun to learn', '[\"Join a network of 100+ hiring managers from top companies.\", \"Get regular updates on job openings, interviews, and referrals.\", \"Build strong industry connections to make yourself visible to recruiters.\", \"Stay one step ahead in job search with WhiteScholars.\", \"Gain community access to industry recruiters.\", \"Participate in placement drives by top companies exclusive for WhiteScholars Students.\"]', 'program_highlights/program-highlight.webp', 1),
(5, 'Network of 100+ hiring partners', 'Connect with a wide network of hiring partners to accelerate your career growth.', '[\"Get access to exclusive job postings.\", \"Participate in WhiteScholars placement drives.\", \"Get guidance from recruitment mentors.\"]', 'program_highlights/program-highlight_lda0uv6.webp', 1),
(6, 'Industry-focused curriculum', 'Our course is designed with real-world relevance in mind.', '[\"Hands-on assignments inspired by actual business challenges.\", \"Updated modules aligned with current industry standards.\"]', 'program_highlights/program-highlight_eXGSBV3.webp', 1);

-- --------------------------------------------------------

--
-- Table structure for table `why_choose`
--

CREATE TABLE `why_choose` (
  `id` bigint(20) NOT NULL,
  `icon` varchar(100) DEFAULT NULL,
  `heading` varchar(255) NOT NULL,
  `text` longtext NOT NULL,
  `course_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `why_choose`
--

INSERT INTO `why_choose` (`id`, `icon`, `heading`, `text`, `course_id`) VALUES
(2, 'why_choose_icons/document.png', 'Hands-On Learning', 'Work on real projects in our data science course in Hyderabad to apply your skills practically.\r\n          ', 1),
(3, 'why_choose_icons/document.png', 'Hands-On Learning', 'Work on real projects in our data science course in Hyderabad to apply your skills practically.\r\n          ', 1),
(4, 'why_choose_icons/document.png', 'Hands-On Learning', 'Work on real projects in our data science course in Hyderabad to apply your skills practically.\r\n          ', 1),
(5, 'why_choose_icons/document.png', 'Hands-On Learning', 'Work on real projects in our data science course in Hyderabad to apply your skills practically.\r\n          ', 1);

-- --------------------------------------------------------

--
-- Table structure for table `why_white_scholars`
--

CREATE TABLE `why_white_scholars` (
  `id` bigint(20) NOT NULL,
  `description` longtext NOT NULL,
  `images` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`images`)),
  `course_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `why_white_scholars`
--

INSERT INTO `why_white_scholars` (`id`, `description`, `images`, `course_id`) VALUES
(2, 'Affordable data science course fees in Hyderabad\r\nRecognized data science certification with placement\r\nIncludes AI course with certification\r\nCovers complete data science syllabus (India standards)\r\nOptions for online, offline, hybrid mode and weekend data science course in Hyderabad\r\nSpecial batches for beginners and freshers\r\nAvailable in online and offline (classroom) modes\r\nFocused on job-ready skills with live projects\r\nGuaranteed internship projects\r\n100% placement assistance till you get placed.', '[\"why_white_scholars_images\\\\GROUPOFPEOPLE-300x200.jpg.webp\", \"why_white_scholars_images\\\\GROUPOFPEOPLE-300x200.jpg.webp\", \"why_white_scholars_images\\\\GROUPOFPEOPLE-300x200.jpg.webp\"]', 1);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `accreditationsandcertification`
--
ALTER TABLE `accreditationsandcertification`
  ADD PRIMARY KEY (`id`),
  ADD KEY `accreditationsandcertification_course_id_67dc94cc_fk_courses_id` (`course_id`);

--
-- Indexes for table `auth_group`
--
ALTER TABLE `auth_group`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  ADD KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`);

--
-- Indexes for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`);

--
-- Indexes for table `auth_user`
--
ALTER TABLE `auth_user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indexes for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  ADD KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`);

--
-- Indexes for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  ADD KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`);

--
-- Indexes for table `career_assistance`
--
ALTER TABLE `career_assistance`
  ADD PRIMARY KEY (`id`),
  ADD KEY `career_assistance_course_id_5f6d65d6_fk_courses_id` (`course_id`);

--
-- Indexes for table `career_transitions`
--
ALTER TABLE `career_transitions`
  ADD PRIMARY KEY (`id`),
  ADD KEY `career_transitions_course_id_c7e0de14_fk_courses_id` (`course_id`);

--
-- Indexes for table `courses`
--
ALTER TABLE `courses`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `slug` (`slug`);

--
-- Indexes for table `course_intro`
--
ALTER TABLE `course_intro`
  ADD PRIMARY KEY (`id`),
  ADD KEY `course_intro_course_id_96de97a3_fk_courses_id` (`course_id`);

--
-- Indexes for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  ADD KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`);

--
-- Indexes for table `django_content_type`
--
ALTER TABLE `django_content_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`);

--
-- Indexes for table `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `django_session`
--
ALTER TABLE `django_session`
  ADD PRIMARY KEY (`session_key`),
  ADD KEY `django_session_expire_date_a5c62663` (`expire_date`);

--
-- Indexes for table `fee_structures`
--
ALTER TABLE `fee_structures`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fee_structures_course_id_79ae8a47_fk_courses_id` (`course_id`);

--
-- Indexes for table `key_highlight`
--
ALTER TABLE `key_highlight`
  ADD PRIMARY KEY (`id`),
  ADD KEY `key_highlight_course_id_af6ca450_fk_courses_id` (`course_id`);

--
-- Indexes for table `listen_our_expert`
--
ALTER TABLE `listen_our_expert`
  ADD PRIMARY KEY (`id`),
  ADD KEY `listen_our_expert_course_id_c8b19d54_fk_courses_id` (`course_id`);

--
-- Indexes for table `mentors`
--
ALTER TABLE `mentors`
  ADD PRIMARY KEY (`id`),
  ADD KEY `mentors_course_id_a1ef7c12_fk_courses_id` (`course_id`);

--
-- Indexes for table `on_campus_classes`
--
ALTER TABLE `on_campus_classes`
  ADD PRIMARY KEY (`id`),
  ADD KEY `on_campus_classes_course_id_94bdb865_fk_courses_id` (`course_id`);

--
-- Indexes for table `our_alumni`
--
ALTER TABLE `our_alumni`
  ADD PRIMARY KEY (`id`),
  ADD KEY `our_alumni_course_id_70bea6af_fk_courses_id` (`course_id`);

--
-- Indexes for table `program_for`
--
ALTER TABLE `program_for`
  ADD PRIMARY KEY (`id`),
  ADD KEY `program_for_course_id_49746e08_fk_courses_id` (`course_id`);

--
-- Indexes for table `program_highlights`
--
ALTER TABLE `program_highlights`
  ADD PRIMARY KEY (`id`),
  ADD KEY `program_highlights_course_id_f02f716b_fk_courses_id` (`course_id`);

--
-- Indexes for table `why_choose`
--
ALTER TABLE `why_choose`
  ADD PRIMARY KEY (`id`),
  ADD KEY `why_choose_course_id_93311915_fk_courses_id` (`course_id`);

--
-- Indexes for table `why_white_scholars`
--
ALTER TABLE `why_white_scholars`
  ADD PRIMARY KEY (`id`),
  ADD KEY `why_white_scholars_course_id_9a76d859_fk_courses_id` (`course_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `accreditationsandcertification`
--
ALTER TABLE `accreditationsandcertification`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `auth_group`
--
ALTER TABLE `auth_group`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_permission`
--
ALTER TABLE `auth_permission`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=85;

--
-- AUTO_INCREMENT for table `auth_user`
--
ALTER TABLE `auth_user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `career_assistance`
--
ALTER TABLE `career_assistance`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `career_transitions`
--
ALTER TABLE `career_transitions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `courses`
--
ALTER TABLE `courses`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `course_intro`
--
ALTER TABLE `course_intro`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;

--
-- AUTO_INCREMENT for table `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=38;

--
-- AUTO_INCREMENT for table `fee_structures`
--
ALTER TABLE `fee_structures`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `key_highlight`
--
ALTER TABLE `key_highlight`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `listen_our_expert`
--
ALTER TABLE `listen_our_expert`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `mentors`
--
ALTER TABLE `mentors`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `on_campus_classes`
--
ALTER TABLE `on_campus_classes`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `our_alumni`
--
ALTER TABLE `our_alumni`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `program_for`
--
ALTER TABLE `program_for`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `program_highlights`
--
ALTER TABLE `program_highlights`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `why_choose`
--
ALTER TABLE `why_choose`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `why_white_scholars`
--
ALTER TABLE `why_white_scholars`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `accreditationsandcertification`
--
ALTER TABLE `accreditationsandcertification`
  ADD CONSTRAINT `accreditationsandcertification_course_id_67dc94cc_fk_courses_id` FOREIGN KEY (`course_id`) REFERENCES `courses` (`id`);

--
-- Constraints for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Constraints for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Constraints for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  ADD CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `career_assistance`
--
ALTER TABLE `career_assistance`
  ADD CONSTRAINT `career_assistance_course_id_5f6d65d6_fk_courses_id` FOREIGN KEY (`course_id`) REFERENCES `courses` (`id`);

--
-- Constraints for table `career_transitions`
--
ALTER TABLE `career_transitions`
  ADD CONSTRAINT `career_transitions_course_id_c7e0de14_fk_courses_id` FOREIGN KEY (`course_id`) REFERENCES `courses` (`id`);

--
-- Constraints for table `course_intro`
--
ALTER TABLE `course_intro`
  ADD CONSTRAINT `course_intro_course_id_96de97a3_fk_courses_id` FOREIGN KEY (`course_id`) REFERENCES `courses` (`id`);

--
-- Constraints for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `fee_structures`
--
ALTER TABLE `fee_structures`
  ADD CONSTRAINT `fee_structures_course_id_79ae8a47_fk_courses_id` FOREIGN KEY (`course_id`) REFERENCES `courses` (`id`);

--
-- Constraints for table `key_highlight`
--
ALTER TABLE `key_highlight`
  ADD CONSTRAINT `key_highlight_course_id_af6ca450_fk_courses_id` FOREIGN KEY (`course_id`) REFERENCES `courses` (`id`);

--
-- Constraints for table `listen_our_expert`
--
ALTER TABLE `listen_our_expert`
  ADD CONSTRAINT `listen_our_expert_course_id_c8b19d54_fk_courses_id` FOREIGN KEY (`course_id`) REFERENCES `courses` (`id`);

--
-- Constraints for table `mentors`
--
ALTER TABLE `mentors`
  ADD CONSTRAINT `mentors_course_id_a1ef7c12_fk_courses_id` FOREIGN KEY (`course_id`) REFERENCES `courses` (`id`);

--
-- Constraints for table `on_campus_classes`
--
ALTER TABLE `on_campus_classes`
  ADD CONSTRAINT `on_campus_classes_course_id_94bdb865_fk_courses_id` FOREIGN KEY (`course_id`) REFERENCES `courses` (`id`);

--
-- Constraints for table `our_alumni`
--
ALTER TABLE `our_alumni`
  ADD CONSTRAINT `our_alumni_course_id_70bea6af_fk_courses_id` FOREIGN KEY (`course_id`) REFERENCES `courses` (`id`);

--
-- Constraints for table `program_for`
--
ALTER TABLE `program_for`
  ADD CONSTRAINT `program_for_course_id_49746e08_fk_courses_id` FOREIGN KEY (`course_id`) REFERENCES `courses` (`id`);

--
-- Constraints for table `program_highlights`
--
ALTER TABLE `program_highlights`
  ADD CONSTRAINT `program_highlights_course_id_f02f716b_fk_courses_id` FOREIGN KEY (`course_id`) REFERENCES `courses` (`id`);

--
-- Constraints for table `why_choose`
--
ALTER TABLE `why_choose`
  ADD CONSTRAINT `why_choose_course_id_93311915_fk_courses_id` FOREIGN KEY (`course_id`) REFERENCES `courses` (`id`);

--
-- Constraints for table `why_white_scholars`
--
ALTER TABLE `why_white_scholars`
  ADD CONSTRAINT `why_white_scholars_course_id_9a76d859_fk_courses_id` FOREIGN KEY (`course_id`) REFERENCES `courses` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
